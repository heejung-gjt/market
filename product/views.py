from django.http.response import JsonResponse
from filter.models import Category
from social.models import Like,Comment
from product.models import Article, Photo
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
from django.db.models import Q
from django.db.models import Count
import json


# main page 
class ProductView(View):

  def get(self, request, *args, **kwargs):
    if request.is_ajax():
      try:
        product = json.loads(request.GET.get('param'))
        print(product)
        articles = Article.objects.filter(Q(name__icontains=product) | Q(content__icontains=product) | Q(category__name__icontains=product)).distinct()
      except:
        articles = ProductFilterService.find_by_not_deleted_article()
      comment_cnt = []
      like_cnt = []
      main_img = []
      writer_profile = []
      for article in articles:
        comment_cnt.append(article.comment.all().count())
        like_cnt.append(article.like.users.all().count())
        writer_profile.append([article.writer.image, article.writer.nickname])
        photo = Photo.objects.filter(article__pk=article.pk).first()
        main_img.append(photo.image.__dict__['name'])
      articles = list(articles.values())
      context = {'image':main_img, 'articles':articles, 'comment_cnt':comment_cnt,'like_cnt':like_cnt,'writer_image':writer_profile}
      return JsonResponse(context, status=200)

    context = {}
    context['category_list'] = ProductFilterService.find_by_all_category()
    context['article_list'] = ProductFilterService.find_by_not_deleted_article()
    return render(request, 'article.html', context)


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
    context = {'category_list':categorys,'state':False}
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

  def post(self, request, *args, **kwargs):
    categorys = ProductFilterService.find_by_all_category()
    category = request.POST.get('sub_menu_pk', None)
    price_from = request.POST.get('product-price-start',0)
    price_to = request.POST.get('product-price-end', 10000000)
    product_sort = request.POST.get('product-sort', None)
    price_from = int(price_from)
    price_to = int(price_to)
    articles = None
    q = Q()
    if category:
      q &= Q(category = category)
    q &= Q(price__range =(price_from, price_to))
    if product_sort:
      if product_sort == '1':
        articles = Article.objects.filter(q).order_by('price')
      elif product_sort == '2':
        articles = Article.objects.filter(q).order_by('-price')
      elif product_sort == '3':
        articles = Article.objects.filter(q, is_deleted=False).annotate(like_count=Count('like__users')).order_by('-like_count','-created_at')
      elif product_sort == '4':
        articles = Article.objects.filter(q, is_deleted=False).annotate(review_count=Count('comment')).order_by('-review_count','-created_at')
    else:
      articles = Article.objects.filter(q).all()
    context = {'article_list':articles,'category_list':categorys}
    return render(request, 'article.html', context)


class SelectDetailView(View):
    def get(self, request, *args, **kwargs):
        pass
    
    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            data = json.loads(request.body)
            price_from = data.get('product-price-start',0)
            price_to = data.get('product-price-end', 10000000)
            product_sort = data.get('product-sort', None)
            category = data.get('category_pk', None)
            category_detail = data.get('sub-menu-pk', None)
            price_from = int(price_from)
            price_to = int(price_to)
            articles = None
            q = Q()

            q &= Q(category = category)
            if category_detail:
                q &= Q(category_detail = category_detail)
            q &= Q(price__range =(price_from, price_to))

            if product_sort:
                if product_sort == '1':
                    articles = Article.objects.filter(q).order_by('price')
                elif product_sort == '2':
                    articles = Article.objects.filter(q).order_by('-price')
                elif product_sort == '3':
                    articles = Article.objects.filter(q, is_deleted=False).annotate(like_count=Count('like__users')).order_by('-like_count','-created_at')
                elif product_sort == '4':
                    articles = Article.objects.filter(q, is_deleted=False).annotate(review_count=Count('comment')).order_by('-review_count','-created_at')
            else:
                articles = Article.objects.filter(q).all()
            comment_cnt = []
            like_cnt = []
            main_img = []
            writer_profile = []
            category_name = Category.objects.filter(pk = category).first().name
            for article in articles:
                comment_cnt.append(article.comment.all().count())
                like_cnt.append(article.like.users.all().count())
                writer_profile.append([article.writer.image, article.writer.nickname])
            for article in articles:
              photo = Photo.objects.filter(article__pk = article.pk).first()
              main_img.append(photo.image.__dict__['name'])
            articles = list(articles.values())
            context = {'image':main_img, 'articles':articles, 'comment_cnt':comment_cnt,'like_cnt':like_cnt,'writer_image':writer_profile,'category_name':category_name}
            return JsonResponse(context)


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

