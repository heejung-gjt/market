from django.db import models
from behaviors import Nameable

# Create your models here.
class Category(Nameable):

  def __str__(self):
    return self.name


class CategoryDetail(Nameable):
  category = models.ManyToManyField(Category, blank=True,related_name='category_detail')
  def __str__(self):
    return self.name