from filter.models import Category, CategoryDetail
from product.models import Article
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import TemplateView,ListView,DetailView
from django.views.generic import View
from .models import Article
from filter.services import ProductDetailService, ProductFilterService
from .services import ProductService
from .dto import ArticleDto
# Create your views here.

class ProductView(ListView):
  model = Article
  template_name = 'article.html'

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['category_list'] = ProductFilterService.find_by_all_category()
    context['article_list'] = ProductFilterService.find_by_all_article()
    return context


class DetailView(DetailView):
  model = Article
  template_name = 'detail.html'

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['article'] = ProductDetailService.get_detail_infor(self.kwargs['pk'])
    categorys = ProductFilterService.find_by_all_category()
    context['category_list'] =categorys
    return context


class ArticleCreateView(View):
  def get(self, request, *args, **kwargs):
    categorys = ProductFilterService.find_by_all_category()
    context = {'category_list':categorys}
    return render(request, 'upload_product.html',context)

  def post(self, request, *args, **kwargs):
    category_pk =request.POST['category_pk']
    article_dto = self._build_article_dto(request)
    ProductService.create(article_dto)
    
    return redirect('filter:category-list',category_pk)

  def _build_article_dto(self, request):
    return ArticleDto(
      name = request.POST['name'],
      category_pk = request.POST['category_pk'],
      content = request.POST['content'],
      image = request.FILES.getlist('image'),
      origin_price = request.POST['origin_price'],
      price = request.POST['price'],
      writer = request.user,
      category_detail_pk = request.POST['category_pk']
    )


class SelectView(View):
  def get(self, request, *args, **kwargs):
    categorys = ProductFilterService.find_by_all_category()
    category_detail_pk = request.GET.get('category_pk')
    category_detail = ProductFilterService.find_by_category_detail(category_detail_pk)
    category = ProductFilterService.find_by_category_title(category_detail_pk)
    context = {'category_list':categorys,'category':category,'state':True,'category_detail':category_detail}
    return render(request, 'upload_product.html',context)
  
  def post(self, request, *args, **kwargs):

    return render(request, 'upload_product.html')