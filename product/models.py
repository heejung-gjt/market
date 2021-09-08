from django.db import models
from user.models import Address, User
from behaviors import Nameable, TimeStampable, Deleteable
from filter.models import CategoryDetail, Category
from utils import upload_get_time_passed

class Article(Nameable, TimeStampable, Deleteable):
  category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='article')
  category_detail = models.ManyToManyField(CategoryDetail,related_name='article',blank=True)
  content = models.TextField()
  origin_price = models.IntegerField(null=True)
  price = models.IntegerField(default=0)
  writer = models.ForeignKey(User, on_delete=models.SET_NULL,null=True, related_name='article')
  # image = models.TextField(null=True, blank=True)
  address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True, related_name='article')

  @property
  def created_string(self):
    created_time = upload_get_time_passed(self.created_at)
    return created_time

class Price(models.Model):
  article = models.OneToOneField(Article, on_delete=models.SET_NULL, null=True, related_name='article_price')
  discount_rate = models.FloatField(default=0)

class Photo(models.Model):
  article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='photo')
  image = models.ImageField(upload_to='image/')

