from product.models import Article
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import TemplateView,ListView,DetailView
from django.views.generic import View
from .models import Article
from filter.services import ProductDetailService, ProductFilterService
from .services import ProductService
from .dto import ArticleDto
# Create your views here.

# listview로 바꿔야함
class ProductView(ListView):
  model = Article
  # context_object_name = 'article_list'
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
      price = request.POST['price'],
      writer = request.user
    )

