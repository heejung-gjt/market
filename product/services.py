from django.shortcuts import get_object_or_404
from .dto import ArticleDto
from .models import Article
from filter.models import Category, CategoryDetail
from .models import Photo


class ProductService():
  @staticmethod
  def create(dto:ArticleDto):
    category = get_object_or_404(Category, pk=dto.category_pk)
    category_detail_name = CategoryDetail.objects.filter(pk = dto.category_detail_pk).first()
    category_detail_obj = Article.objects.filter(category_detail__name = category_detail_name).first()
    article = Article.objects.create(
      name = dto.name,
      category = category,
      content = dto.content,
      origin_price = dto.origin_price,
      price = dto.price,
      writer = dto.writer
    )
    
    if category_detail_obj is None:
      article.category_detail.add(category_detail_name)

    for img in dto.image:
      photo = Photo.objects.create(
        article = article,
        image = img
      )
      photo.save()

    
