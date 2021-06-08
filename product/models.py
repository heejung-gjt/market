from django.db import models
from django.contrib.auth.models import User
from behaviors import Nameable, TimeStampable, Deleteable
from filter.models import CategoryDetail, Category
# Create your models here.


class Article(Nameable, TimeStampable, Deleteable):
  category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='article')
  category_detail = models.ManyToManyField(CategoryDetail,related_name='article',blank=True)
  content = models.TextField()
  origin_price = models.IntegerField(null=True)
  price = models.IntegerField(default=0)
  writer = models.ForeignKey(User, on_delete=models.SET_NULL,null=True, related_name='article')
  

class Price(models.Model):
  article = models.OneToOneField(Article, on_delete=models.SET_NULL, null=True, related_name='article_price')
  discount_rate = models.FloatField(default=0)

class Photo(models.Model):
  article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='photo')
  image = models.ImageField(upload_to='image/')

