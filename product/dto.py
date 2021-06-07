from dataclasses import dataclass
from filter.models import Category, CategoryDetail
from django.contrib.auth.models import User


@dataclass
class ArticleDto():
  name:str
  category_pk:str
  content:str
  image:list
  origin_price:int
  price:int
  writer:User
  category_detail_pk:str

