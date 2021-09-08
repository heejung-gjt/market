from django.http import request
from .dto import ArticleDto, EditDto
from .models import Article,Price
from social.models import Like
from filter.services import CategoryFilterService, ProductFilterService
from .models import Photo
from utils import calculate_price
from user.utils import context
import time


# product crud 
class ProductService():

  @staticmethod
  def create(dto:ArticleDto):
    category_detail_name = CategoryFilterService.find_by_category_detail(dto.category_detail_pk)
    category_pk = CategoryFilterService.find_by_category_detail(dto.category_pk).category.pk
    category = CategoryFilterService.find_by_filter_category(category_pk)
    discount_rate = calculate_price(dto.origin_price, dto.price)

    if not dto.content or not dto.image or not dto.price or not dto.origin_price or not dto.name:
      result = context(True, '모든 내용을 작성해주세요 !')
      return result
      
    if discount_rate == -1:
      result = context(True, '정상적인 금액을 입력해주세요 !')
      return result
    
    
    article = Article.objects.create(
      name = dto.name,
      category = category,
      content = dto.content,
      origin_price = dto.origin_price,
      price = dto.price,
      writer = dto.writer,
      address = dto.writer.address,
      created_at = time.time()
    )
    article.category_detail.add(category_detail_name)
    
    Price.objects.create(
      article = article,
      discount_rate = discount_rate 
    )
    Like.objects.create(
        article = article
        )

    for img in dto.image:
      photo = Photo.objects.create(
        article = article,
        image = img
      )  
      photo.save()


    result = context(False, 'completed')
    return result
    
  
  @staticmethod
  def edit(dto:EditDto):
    category = CategoryFilterService.find_by_filter_category(dto.category_pk)
    article = ProductFilterService.find_article_infor(dto.article_pk)
    discount_rate = calculate_price(dto.origin_price, dto.price)
  
    Article.objects.filter(pk=dto.article_pk).update(
      category = category,
      name = dto.name,
      content = dto.content,
      origin_price = dto.origin_price,
      price = dto.price,
      writer = dto.writer,
      
    )
    discount_rate = calculate_price(dto.origin_price, dto.price)
    if discount_rate == -1:
      return discount_rate
    
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
    return False


    
