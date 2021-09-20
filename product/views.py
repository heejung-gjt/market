from django.http.response import JsonResponse
from utils import paginator
from filter.models import Category
from social.models import Like,Comment
from product.models import Article, Photo
from django.shortcuts import redirect, render
from django.views.generic import ListView,DetailView
from django.views.generic import View
from user.models import User
from .models import Article, Price
from filter.services import ProductFilterService
from .services import ProductService
from .dto import ArticleDto, EditDto
from django.utils.datastructures import MultiValueDictKeyError
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from django.db.models import Q
from django.db.models import Count
from filter.models import Category, CategoryDetail
import json


# main page 
class ProductView(View):
  def get(self, request, *args, **kwargs):
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
    context = {}
    context['category_list'] = ProductFilterService.find_by_all_category()
    article_list = ProductFilterService.find_by_not_deleted_article()
    # context['article_list'] = article_list
    page = request.GET.get('page', '1')
    articles, page_range = paginator(article_list, page, 9)
    context['article_list'] = articles
    context['page_range'] = page_range
    context['is_page'] = True
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


# product category
class ArticleCategoryUploadView(View):
  def get(self, request, *args, **kwargs):
    categorys = ProductFilterService.find_by_all_category()
    category_detail_pk = request.GET.get('category_pk')
    category_detail = ProductFilterService.find_by_category_detail(category_detail_pk)
    category = ProductFilterService.find_by_category_title(category_detail_pk)
    context = {'category_list':categorys,'category':category,'state':True,'category_detail':category_detail}
    return render(request, 'upload_product.html', context)
  

# product sub select menu
class SelectView(View):
  """
  date: 0915
  이미지 업로드할때 이곳으로 get요청 들어옴,, 수정이 필요해보임.. (수정함)
  """
  def get(self, request, *args, **kwargs):
    categorys = ProductFilterService.find_by_all_category()
    category = self.request.GET.get('sub-menu-pk', None)
    price_from = self.request.GET.get('price-start',0)
    price_to = self.request.GET.get('price-end', 10000000)
    product_sort = self.request.GET.get('sort', None)
    price_from = int(price_from)
    price_to = int(price_to)
    articles = None
    q = Q()
    if category:
      q &= Q(category = category)
    q &= Q(price__range =(price_from, price_to))
    if product_sort:
      if product_sort == '1':
        articles = Article.objects.filter(q).order_by('-created_at')
      if product_sort == '2':
        articles = Article.objects.filter(q).order_by('created_at')
      if product_sort == '3':
        articles = Article.objects.filter(q).order_by('price')
      elif product_sort == '4':
        articles = Article.objects.filter(q).order_by('-price')
      elif product_sort == '5':
        articles = Article.objects.filter(q, is_deleted=False).annotate(like_count=Count('like__users')).order_by('-like_count','-created_at')
      elif product_sort == '6':
        articles = Article.objects.filter(q, is_deleted=False).annotate(review_count=Count('comment')).order_by('-review_count','-created_at')
    else:
      articles = Article.objects.filter(q).order_by('-created_at')
    page = request.GET.get('page', '1')
    articles, page_range = paginator(articles, page, 9)

    context = {'sort':product_sort,'pk':category,'start':price_from,'end':price_to, 'article_list':articles,'category_list':categorys,'is_page':False,'page_range':page_range}
    return render(request, 'article.html', context)


class SelectDetailView(View):
    def get(self, request, *args, **kwargs):
        price_from = self.request.GET.get('price-start',0)
        price_to = self.request.GET.get('price-end', 10000000)
        product_sort = self.request.GET.get('sort', None)
        category = self.request.GET.get('category', None)
        category_title = Category.objects.get(pk=category)
        categorys = ProductFilterService.find_by_all_category()
        print('ddddddd')
        category_detail = self.request.GET.get('sub-menu', None)
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
        category_sub_list = CategoryDetail.objects.filter(category__pk = category)
        category_name = Category.objects.filter(pk = category).first().name
        page = request.GET.get('page', '1')
        articles, page_range = paginator(articles, page, 9)
        context = {'category_list':categorys,'category_sub_list':category_sub_list, 'articles':articles,'page_range':page_range,'sort':product_sort,'pk':category,'sub_pk':category_detail,'start':price_from,'end':price_to,'category_title':category_title,'category_name':category_name}
        return render(request, 'category-list.html',context)
    

class ProductFilterView(View):
  """
  date:0915 
  검색기능 검색 요청 들어오는 View
  incontains기능 사용 x
  """
  def get(self, request, *args, **kwargs):
    categorys = ProductFilterService.find_by_all_category()
    search_keyword = self.request.GET.get('search','')
    articles = Article.objects.filter(Q(name__icontains=search_keyword) | Q(content__icontains=search_keyword) | Q(category__name__icontains=search_keyword)).distinct().order_by('-created_at')
    article_sum = articles.count()
    context = {'article_sum':article_sum,'article_list':articles, 'category_list':categorys, 'keyword':search_keyword}
    page = request.GET.get('page', '1')
    articles, page_range = paginator(articles, page, 12)
    context['article_list'] = articles
    context['page_range'] = page_range
    return render(request, 'product-filter.html', context)


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

