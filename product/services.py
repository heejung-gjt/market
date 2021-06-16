from django.shortcuts import get_object_or_404
from .dto import ArticleDto, EditDto
from .models import Article,Price
from social.models import Comment, Like
from filter.models import Category, CategoryDetail
from filter.services import CategoryFilterService
from .models import Photo
from .utils import calculate_price


# product crud 
class ProductService():

  @staticmethod
  def create(dto:ArticleDto):
    category_detail_name = CategoryFilterService.find_by_category_detail(dto.category_detail_pk)
    category_pk = CategoryFilterService.find_by_category_detail(dto.category_pk).category.pk
    category = CategoryFilterService.find_by_filter_category(category_pk)
    
    article = Article.objects.create(
      name = dto.name,
      category = category,
      content = dto.content,
      origin_price = dto.origin_price,
      price = dto.price,
      writer = dto.writer
    )
    
    discount_rate = calculate_price(dto.origin_price, dto.price)
    
    Price.objects.create(
      article = article,
      discount_rate = discount_rate 
    )

    Like.objects.create(
        article = article
        )
    
    article.category_detail.add(category_detail_name)

    for img in dto.image:
      photo = Photo.objects.create(
        article = article,
        image = img
      )  
      photo.save()
    
  
  @staticmethod
  def edit(dto:EditDto):
    category = get_object_or_404(Category, pk=dto.category_pk)
    article = Article.objects.filter(pk = dto.article_pk).first()
    Article.objects.filter(pk=dto.article_pk).update(
      category = category,
      name = dto.name,
      content = dto.content,
      origin_price = dto.origin_price,
      price = dto.price,
      writer = dto.writer
    )
    discount_rate = calculate(dto.origin_price, dto.price)
    Price.objects.filter(article__pk = dto.article_pk).update(
      article = article,
      discount_rate = discount_rate 
    )
    
    if dto.image:
      Photo.objects.filter(article__pk = dto.article_pk).delete() 

      for img in dto.image:
        Photo.objects.filter(article__pk = dto.article_pk).create(
          article = article,
          image = img
          )  


    
