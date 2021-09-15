from user.models import User
from product.models import Article
from django.shortcuts import get_object_or_404
from filter.models import Category,CategoryDetail
from django.db.models import Count


class ProductFilterService():

  @staticmethod
  def find_by_product_list(category_pk):
    articles = get_object_or_404(Category, pk = category_pk).article
    articles = Category.objects.get(pk=category_pk).article.all()
    print(articles)
    return articles
  
  @staticmethod
  def find_by_category_title(category_pk):
    category_title = get_object_or_404(Category, pk=category_pk)
    return category_title

  @staticmethod
  def find_by_all_category():
    category_list = Category.objects.all()
    return category_list
  
  @staticmethod
  def find_by_latest_article():
    article_list = Article.objects.filter(is_deleted = False).order_by('-created_at')
    return article_list

  @staticmethod
  def get_order_by_comment_count():
    article = Article.objects.filter(is_deleted=False).annotate(review_count=Count('comment')).order_by('-review_count','-created_at')
    return article

  @staticmethod
  def get_order_by_like_count():
    article = Article.objects.filter(is_deleted=False).annotate(like_count=Count('like')).order_by('-like_count','-created_at')
    return article
  
  @staticmethod
  def get_order_by_user_article(request):
    user = request.user
    article = Article.objects.filter(writer__pk = user.pk, is_deleted=False).order_by('-created_at')
    return article

  @staticmethod
  def find_by_all_article():
    article_list = Article.objects.all()
    return article_list

  @staticmethod
  def find_by_not_deleted_article():
    article_list = Article.objects.filter(is_deleted = False).order_by('-created_at')
    return article_list
  
  @staticmethod
  def find_not_deleted_user_article_list(**kwargs):
    articles = Article.objects.filter(is_deleted=kwargs['is_deleted'], writer=kwargs['writer'])
    return articles

  @staticmethod
  def find_by_filter_article(user):
    articles = Article.objects.filter(writer__pk = user.pk)
    return articles

  @staticmethod
  def find_by_category_detail(pk):
    category_detail = CategoryDetail.objects.filter(category__pk = pk)
    return category_detail

  @staticmethod
  def find_by_category_pk_in_category_detail(category_detail_pk):
    category_pk = CategoryDetail.objects.filter(pk = category_detail_pk).first().category.pk
    return category_pk
  
  @staticmethod
  def find_article_infor(pk):
    article = get_object_or_404(Article, pk = pk)
    return article


class UserFilterService():

  @staticmethod
  def find_by_user(pk):
    print('접근은함')
    user = User.objects.filter(pk=pk).first()
    return user


class CategoryFilterService():

  @staticmethod
  def find_by_category_detail(pk):
    category =  CategoryDetail.objects.filter(pk= pk).first() 
    return category

  @staticmethod
  def find_by_filter_category(pk):
    category = get_object_or_404(Category, pk = pk)
    return category