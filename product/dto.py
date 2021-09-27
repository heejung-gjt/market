from dataclasses import dataclass
from django.contrib.auth.models import User


@dataclass
class ProductDto():
    name:str
    category_pk:str
    content:str
    image:list
    origin_price:int
    price:int
    writer:User
    category_detail_pk:int


@dataclass
class EditDto():
    name:str
    category_pk:str
    content:str
    image:list
    origin_price:int
    price:int
    writer:User
    article_pk:str


@dataclass
class ProductPkDto():
    article_pk:int


@dataclass
class ProductCategoryDto():
    category_detail_pk:int


@dataclass
class ProductFilterDto():
    category_pk:int
    price_from:int
    price_to:int
    product_sort:int


@dataclass
class ProductSubFilterDto():
    price_from:int
    price_to:int
    product_sort:int
    category:str
    category_detail:str
    

@dataclass
class ProductSearchDto():
    search_keyword:str

