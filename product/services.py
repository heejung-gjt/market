from django.shortcuts import get_object_or_404
from .dto import ArticleDto, EditDto
from .models import Article,Price
from filter.models import Category, CategoryDetail
from .models import Photo

# product sale percentage function
def calculate(origin_price, sale_price):
  # origin_price = origin_price
  price = sale_price
  price_gap = int(origin_price) - int(price)
  real_sale = int(price_gap)/int(origin_price)*100
  discount_rate = round(real_sale, 1)
  return discount_rate


# product crud 
class ProductService():

  @staticmethod
  def create(dto:ArticleDto):
    category_detail_name = CategoryDetail.objects.filter(pk = dto.category_detail_pk).first()
    category_detail_obj = Article.objects.filter(category_detail__name = category_detail_name).first()
    # print('obj',category_detail_obj)
    category_pk = CategoryDetail.objects.filter(pk = dto.category_pk).first().category.pk
    category = get_object_or_404(Category, pk=category_pk)
    article = Article.objects.create(
      name = dto.name,
      category = category,
      content = dto.content,
      origin_price = dto.origin_price,
      price = dto.price,
      writer = dto.writer
    )
    
    discount_rate = calculate(dto.origin_price, dto.price)
    Price.objects.create(
      article = article,
      discount_rate = discount_rate 
    )
    
    # if category_detail_obj is None:
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


    
