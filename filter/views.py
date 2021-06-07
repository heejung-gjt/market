from product.views import DetailView
from django.shortcuts import redirect, render
from django.views.generic import TemplateView, ListView
from .models import Category
from filter.services import ProductFilterService
# Create your views here.



class CategoryView(ListView):
  model = Category
  context_object_name = 'category_list'
  template_name = 'category.html'

  
class CategoryListView(DetailView):
  model = Category
  template_name = 'category-list.html'

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)

    context['category_articles'] = ProductFilterService.find_by_product_list(self.kwargs['pk'])
    context['category_title'] = ProductFilterService.find_by_category_title(self.kwargs['pk'])
    context['category_list'] = ProductFilterService.find_by_all_category()
    return context