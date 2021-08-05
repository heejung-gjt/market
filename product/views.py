from filter.models import Category
from social.models import Like,Comment
from product.models import Article
from django.shortcuts import redirect, render
from django.views.generic import ListView,DetailView
from django.views.generic import View
from user.models import User
from .models import Article
from filter.services import ProductFilterService
from .services import ProductService
from .dto import ArticleDto, EditDto
from django.utils.datastructures import MultiValueDictKeyError
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
import json


# main page 
class ProductView(ListView):
  model = Article
  template_name = 'article.html'

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['category_list'] = ProductFilterService.find_by_all_category()
    context['article_list'] = ProductFilterService.find_by_not_deleted_article()
    return context


# product detail page
class DetailView(DetailView):

  def get(self, request, **kwargs):
    article_pk = self.kwargs['pk']
    context={}
    context['article'] = ProductFilterService.find_article_infor(article_pk)
    like = Like.objects.filter(article__pk = kwargs['pk']).first()
    context['category_list'] = ProductFilterService.find_by_all_category()
    comment_list = [
      {
        'writer':comment.writer,
        'pk':comment.pk,
        'username':User.objects.get(pk=comment.writer.pk).nickname,
        'content':comment.content,
        'image_url':comment.writer.image,
        'writer_nickname':comment.writer.nickname,
        're_comment':comment.re_comment.all(),
        'comment_obj':comment
      } for comment in Comment.objects.filter(article__pk = article_pk)
    ]
    context['comment_list'] = comment_list
    
    if like is not None:
        if request.user in like.users.all(): 
          context['is_liked'] = True
        else:
          context['is_liked'] = False
    

    return render(request,'detail.html',context)


# create product
class ArticleCreateView(LoginRequiredMixin,generic.View):
  login_url='/user/signin'
  redirect_field_name=None
  
  def get(self, request, *args, **kwargs):
    categorys = ProductFilterService.find_by_all_category()
    context = {'category_list':categorys}

    return render(request, 'upload_product.html',context)

  def post(self, request, *args, **kwargs):
      try:
        category_detail_pk =request.POST['category_pk']
      except MultiValueDictKeyError:
        categorys = ProductFilterService.find_by_all_category()
        context = {'error':{'state':True,'msg':'카테고리를 선택해주세요 !'},'category_list':categorys}
        return render(request, 'upload_product.html',context)

      article_dto = self._build_article_dto(request)
      category_pk = ProductFilterService.find_by_category_pk_in_category_detail(category_detail_pk)
      context = ProductService.create(article_dto)

      if context['error']['state']:
        categorys = ProductFilterService.find_by_all_category()
        context['category_list'] = categorys
        return render(request, 'upload_product.html',context)

      return redirect('filter:category-list',category_pk)
      
  def _build_article_dto(self, request):
    return ArticleDto(
      name = request.POST['name'],
      category_pk = request.POST['category_pk'],
      content = request.POST['content'],
      image = request.FILES.getlist('image'),
      origin_price = request.POST['origin_price'],
      price = request.POST['price'],
      writer = request.user,
      category_detail_pk = request.POST['category_pk']
    )


# product sub select menu
class SelectView(View):
  def get(self, request, *args, **kwargs):
    categorys = ProductFilterService.find_by_all_category()
    category_detail_pk = request.GET.get('category_pk')
    category_detail = ProductFilterService.find_by_category_detail(category_detail_pk)
    category = ProductFilterService.find_by_category_title(category_detail_pk)
    context = {'category_list':categorys,'category':category,'state':True,'category_detail':category_detail}
    return render(request, 'upload_product.html',context)


# product edit
class EditView(View):
  def get(self, request, *args, **kwargs):
    article_pk = kwargs['pk']
    article = ProductFilterService.find_article_infor(article_pk)
    categorys = ProductFilterService.find_by_all_category()
    context = {'category_list':categorys,'article':article}
    return render(request, 'edit.html',context)

  def post(self,request,*args, **kwargs):
    article_dto = self._build_edit_article_dto(request)
    ProductService.edit(article_dto)

    return redirect('home')

  def _build_edit_article_dto(self, request):
    category = Article.objects.filter(pk=self.kwargs['pk']).first().category
    category_pk = Category.objects.filter(name=category).first().pk

    return EditDto(
      name = request.POST['name'],
      category_pk = category_pk,
      content = request.POST['content'],
      image = request.FILES.getlist('image'),
      origin_price = request.POST['origin_price'],
      price = request.POST['price'],
      writer = request.user,
      article_pk = self.kwargs['pk']
    )


# article delete
class DeleteView(View):
  def get(self, request, *args, **kwargs):
    Article.objects.filter(pk=kwargs['pk']).update(
      is_deleted = True
    )
    
    return redirect('product:article')

