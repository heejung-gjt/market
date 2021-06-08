from filter.models import Category, CategoryDetail
from product.models import Article
from django.shortcuts import redirect, render
from django.views.generic import ListView,DetailView
from django.views.generic import View
from .models import Article
from filter.services import ProductFilterService
from .services import ProductService
from .dto import ArticleDto, EditDto


# main page 
class ProductView(ListView):
  model = Article
  template_name = 'article.html'

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['category_list'] = ProductFilterService.find_by_all_category()
    # context['article_list'] = ProductFilterService.find_by_all_article()
    # context['article_list'] = Article.object.filter()
    context['article_list'] = ProductFilterService.find_by_not_deleted_article()
    
    return context

# product detail page
class DetailView(DetailView):
  model = Article
  template_name = 'detail.html'

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['article'] = ProductFilterService.get_detail_infor(self.kwargs['pk'])
    categorys = ProductFilterService.find_by_all_category()
    context['category_list'] =categorys
    return context

# create product
class ArticleCreateView(View):
  def get(self, request, *args, **kwargs):
    categorys = ProductFilterService.find_by_all_category()
    context = {'category_list':categorys}

    return render(request, 'upload_product.html',context)

  def post(self, request, *args, **kwargs):
    category_detail_pk =request.POST['category_pk']
    article_dto = self._build_article_dto(request)
    category_pk = ProductFilterService.find_by_category_pk_in_category_detail(category_detail_pk)
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


# product sub select menu
class SelectView(View):
  def get(self, request, *args, **kwargs):
    categorys = ProductFilterService.find_by_all_category()
    category_detail_pk = request.GET.get('category_pk')
    category_detail = ProductFilterService.find_by_category_detail(category_detail_pk)
    category = ProductFilterService.find_by_category_title(category_detail_pk)
    context = {'category_list':categorys,'category':category,'state':True,'category_detail':category_detail}
    
    return render(request, 'upload_product.html',context)


# product edit
class EditView(View):
  def get(self, request, *args, **kwargs):
    article = ProductFilterService.get_detail_infor(kwargs['pk'])
    context = {'article':article}
    return render(request, 'edit.html',context)

  def post(self,request,*args, **kwargs):
    article_dto = self._build_edit_article_dto(request)
    ProductService.edit(article_dto)

    return redirect('home')

  def _build_edit_article_dto(self, request):
    category = Article.objects.filter(pk=self.kwargs['pk']).first().category
    category_pk = Category.objects.filter(name=category).first().pk

    return EditDto(
      name = request.POST['name'],
      category_pk = category_pk,
      content = request.POST['content'],
      image = request.FILES.getlist('image'),
      origin_price = request.POST['origin_price'],
      price = request.POST['price'],
      writer = request.user,
      article_pk = self.kwargs['pk']
    )


# article delete
class DeleteView(View):
  def get(self, request, *args, **kwargs):
    Article.objects.filter(pk=kwargs['pk']).update(
      is_deleted = True
    )
    
    return redirect('product:article')