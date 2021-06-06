from django.shortcuts import get_object_or_404
from .dto import ArticleDto
from .models import Article
from filter.models import Category
from .models import Photo


class ProductService():
  @staticmethod
  def create(dto:ArticleDto):
    category = get_object_or_404(Category, pk=dto.category_pk)
    # result = {'error':{'state':False},'msg':''}
    article = Article.objects.create(
      name = dto.name,
      category = category,
      content = dto.content,
      price = dto.price,
      writer = dto.writer
    )

    for img in dto.image:
      photo = Photo.objects.create(
        article = article,
        image = img
      )
      photo.save()
      # photo = Photo()
      # photo.article = article
      # photo.image = img
      # photo.save()
    
