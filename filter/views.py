from product.models import Article
from product.views import DetailView
from django.shortcuts import redirect, render
from django.views.generic import TemplateView, ListView
from .models import Category, CategoryDetail
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
    context['sub_state'] = False
    context['category_articles'] = ProductFilterService.find_by_product_list(self.kwargs['pk'])
    context['category_title'] = ProductFilterService.find_by_category_title(self.kwargs['pk'])
    context['category_list'] = ProductFilterService.find_by_all_category()
    context['category_sub_list'] = CategoryDetail.objects.filter(category__pk = self.kwargs['pk'])
    return context

# show sub menu article
class CategorySubListView(DetailView):
  model = Category
  template_name = 'category-list.html'

  def get(self,request,*args, **kwargs):
    context = {}
    context['sub_state'] = True
    if request.GET.get('sub_menu_pk') == '0':
      articles = Article.objects.filter(category__pk = kwargs['pk'], is_deleted=False).all()
    else:
      articles = Article.objects.filter(category_detail__pk = request.GET.get('sub_menu_pk'), is_deleted=False).all()
    context['articles'] = articles
    context['category_sub_list'] = CategoryDetail.objects.filter(category__pk = kwargs['pk'])
    context['category_articles'] = ProductFilterService.find_by_product_list(self.kwargs['pk'])
    context['category_title'] = ProductFilterService.find_by_category_title(self.kwargs['pk'])
    # context['category_list'] = ProductFilterService.find_by_all_category()
    categorys = ProductFilterService.find_by_all_category()
    context['category_list'] =categorys
    return render(request, 'category-list.html',context)

