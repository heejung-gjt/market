from dataclasses import dataclass
from filter.models import Category
from django.contrib.auth.models import User


@dataclass
class ArticleDto():
  name:str
  category_pk:str
  content:str
  image:list
  price:int
  writer:User

