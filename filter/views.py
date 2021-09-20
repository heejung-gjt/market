from product.models import Article
from product.views import DetailView
from django.shortcuts import redirect, render
from django.views.generic import TemplateView, ListView
from .models import Category, CategoryDetail
from filter.services import ProductFilterService
from utils import paginator
# Create your views here.


class CategoryView(ListView):
  model = Category
  context_object_name = 'category_list'
  template_name = 'category.html'

  
class CategoryListView(DetailView):
  def get(self, request, **kwargs):
    context = {}
    articles = ProductFilterService.find_by_product_list(self.kwargs['pk'])
    context['sub_state'] = False
    page = request.GET.get('page', '1')
    articles, page_range = paginator(articles, page, 9) 
    context['articles'] = articles
    context['page_range'] = page_range
    context['category_title'] = ProductFilterService.find_by_category_title(self.kwargs['pk'])
    context['category_list'] = ProductFilterService.find_by_all_category()
    context['category_sub_list'] = CategoryDetail.objects.filter(category__pk = self.kwargs['pk'])
    context['sub_state'] = False
    return render(request, 'category-list.html',context)

# show sub menu article
class CategorySubListView(DetailView):
  model = Category
  template_name = 'category-list.html'

  def get(self,request,*args, **kwargs):
    context = {}
    # context['state'] = False
    context['sub_state'] = True
    if request.GET.get('sub_menu_pk') == '0':
      articles = Article.objects.filter(category__pk = kwargs['pk'], is_deleted=False).all()
    else:
      articles = Article.objects.filter(category_detail__pk = request.GET.get('sub_menu_pk'), is_deleted=False).all()
    context['articles'] = articles
    context['category_sub_list'] = CategoryDetail.objects.filter(category__pk = kwargs['pk'])
    context['category_articles'] = ProductFilterService.find_by_product_list(self.kwargs['pk'])
    context['category_title'] = ProductFilterService.find_by_category_title(self.kwargs['pk'])
    categorys = ProductFilterService.find_by_all_category()
    context['category_list'] =categorys
    return render(request, 'category-list.html',context)


class CategoryFilterListView(ListView):
    # model = Category
    # template_name = 'article.html'

  def get(self,request,*args, **kwargs):
      context = {}
      # context['state'] = False
      if request.GET.get('social-clicked_pk') == '1':
        context['category_list'] = ProductFilterService.find_by_all_category()
        context['article_list'] = ProductFilterService.find_by_latest_article()
        return render(request, 'article.html',context)
      elif request.GET.get('social-clicked_pk') == '2':
        context['category_list'] = ProductFilterService.find_by_all_category()
        context['article_list'] = ProductFilterService.get_order_by_comment_count()
        return render(request, 'article.html',context)
      elif request.GET.get('social-clicked_pk') == '3':
        context['category_list'] = ProductFilterService.find_by_all_category()
        context['article_list'] = ProductFilterService.get_order_by_like_count()
        return render(request, 'article.html',context)
      elif request.GET.get('social-clicked_pk') == '4':
        context['category_list'] = ProductFilterService.find_by_all_category()
        context['article_list'] = ProductFilterService.get_order_by_user_article(request)
        return render(request, 'article.html',context)
      else:
        context['category_list'] = ProductFilterService.find_by_all_category()
        context['article_list'] = ProductFilterService.find_by_not_deleted_article()
        return render(request, 'article.html',context)
