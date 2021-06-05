from django.shortcuts import render
from django.views.generic import TemplateView
# Create your views here.

# listview로 바꿔야함
class ProductView(TemplateView):

  template_name = 'article.html'

class CategoryView(TemplateView):
  template_name = 'category.html'

class DetailView(TemplateView):
  template_name = 'detail.html'