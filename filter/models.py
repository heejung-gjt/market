from django.db import models
from behaviors import Nameable

# Create your models here.
class Category(Nameable):

  def __str__(self):
    return self.name


class CategoryDetail(Nameable):
  category = models.ForeignKey(Category,on_delete=models.CASCADE ,related_name='category')
  def __str__(self):
    return self.name