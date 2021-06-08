from product.models import Article
from django.shortcuts import get_object_or_404
from filter.models import Category,CategoryDetail


# proudcts filter 
class ProductFilterService():

  @staticmethod
  def find_by_product_list(category_pk):
    category_articles = get_object_or_404(Category, pk = category_pk).article
    return category_articles
  
  @staticmethod
  def find_by_category_title(category_pk):
    category_title = get_object_or_404(Category, pk=category_pk)
    return category_title

  @staticmethod
  def find_by_all_category():
    category_list = Category.objects.all()
    return category_list
  
  @staticmethod
  def find_by_all_article():
    article_list = Article.objects.all()
    return article_list

  @staticmethod
  def find_by_not_deleted_article():
    article_list = Article.objects.filter(is_deleted = False)
    return article_list

  @staticmethod
  def find_by_filter_article(user):
    articles = Article.objects.filter(writer__pk = user.pk)
    return articles

  @staticmethod
  def find_by_category_detail(category_detail_pk):
    category_detail = CategoryDetail.objects.filter(category__pk=category_detail_pk)
    return category_detail

  @staticmethod
  def find_by_category_pk_in_category_detail(category_detail_pk):
    category_pk = CategoryDetail.objects.filter(pk = category_detail_pk).first().category.pk
    return category_pk
  
  @staticmethod
  def get_detail_infor(article_pk):
    article = Article.objects.filter(pk=article_pk).first()
    return article
