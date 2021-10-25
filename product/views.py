from utils import context_infor
from django.shortcuts import redirect, render
from django.views.generic import DetailView
from django.views.generic import View
from .models import Article
from filter.models import Category
from product.models import Article
from .services import ProductService
from product.services import ProductService
from filter.services import ProductFilterService
from django.utils.datastructures import MultiValueDictKeyError
from django.contrib.auth.mixins import LoginRequiredMixin
from .dto import (
    ProductCategoryDto, ProductDto, EditDto, ProductFilterDto, ProductPkDto, 
    ProductSearchDto, ProductSubFilterDto)


# main page 
class ProductView(View):

    def get(self, request, *args, **kwargs):
        # articles = ProductFilterService.find_by_not_deleted_article()
        context = ProductService.get_product_infor(request)
        return render(request, 'article.html', context)


# product detail page
class ProductDetailView(DetailView):
    
    def get(self, request, **kwargs):
        data = self._build_article_pk()
        context = ProductService.get_detail_infor(request, data)
        return render(request,'detail.html',context)

    def _build_article_pk(self):
        return ProductPkDto(
            article_pk = self.kwargs['pk']
        )


class ProductCreateView(LoginRequiredMixin, View):
    login_url='/user/signin'
    redirect_field_name=None

    def get(self, request, *args, **kwargs):
        categorys = ProductFilterService.find_by_all_category()
        context = context_infor(category_list = categorys, state = False)
        return render(request, 'upload_product.html',context)

    def post(self, request, *args, **kwargs):
        try:
            data = self._build_article_dto(request)
            context = ProductService.create(data)
            if context['state']:
                categorys = ProductFilterService.find_by_all_category()
                context = context_infor(category_list = categorys)
                return render(request, 'upload_product.html',context)
        except MultiValueDictKeyError:
            category_list = ProductFilterService.find_by_all_category()
            context = context_infor(state = True, msg = '카테고리를 선택해주세요 !', category_list = category_list)
            return render(request, 'upload_product.html',context)
        return redirect('filter:category-list',context['category_pk'])
        
    def _build_article_dto(self, request):
        return ProductDto(
            name = request.POST['name'],
            category_pk = request.POST['category_pk'],
            content = request.POST['content'],
            image = request.FILES.getlist('image'),
            origin_price = request.POST['origin_price'],
            price = request.POST['price'],
            writer = request.user,
            category_detail_pk = request.POST['category_pk']
        )


# upload product category
class ProductCategoryUploadView(View):
  
    def get(self, request, *args, **kwargs):
        data = self._build_product_category_dto(request)
        context = ProductService.get_category_detail(data)
        return render(request, 'upload_product.html', context)

    def _build_product_category_dto(self, request):
        return ProductCategoryDto(
            category_detail_pk = request.GET.get('category_pk')
        )


# select product sub menu
class FilterProductView(View):

    def get(self, request, *args, **kwargs):
        data = self._build_product_filter_dto(request)
        context = ProductFilterService.get_filter_product_infor(request, data)
        return render(request, 'article.html', context)

    def _build_product_filter_dto(self, request):
        return ProductFilterDto(
            category_pk = request.GET.get('sub-menu-pk', 0),
            price_from = request.GET.get('price-start',0),
            price_to = request.GET.get('price-end', 10000000),
            product_sort = request.GET.get('sort', None)
        )


class FilterSubProductView(View):

    def get(self, request, *args, **kwargs):
        data = self._build_sub_product_dto(request)
        context = ProductFilterService.get_filter_sub_product_infor(request, data)
        return render(request, 'category-list.html',context)

    def _build_sub_product_dto(self, request):
        return ProductSubFilterDto(
            price_from = request.GET.get('price-start',0),
            price_to = request.GET.get('price-end', 10000000),
            product_sort = request.GET.get('sort', None),
            category = request.GET.get('category', None),
            category_detail = request.GET.get('sub-menu', 0)
        )
    

class ProductSearchView(View):

    def get(self, request, *args, **kwargs):
        data = self._build_product_search_infor(request)
        context = ProductService.get_search_product_infor(request, data)
        return render(request, 'product-filter.html', context)
    
    def _build_product_search_infor(self, request):
        return ProductSearchDto(
            search_keyword = request.GET.get('search', '')
        )


class ProductEditView(View):

    def get(self, request, *args, **kwargs):
        article = ProductFilterService.find_article_infor(kwargs['pk'])
        categorys = ProductFilterService.find_by_all_category()
        context = context_infor(category_list = categorys, article = article)
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
        data = self._build_product_delete_dto()
        context = ProductService.delete(data)
        return redirect('product:article')

    def _build_product_delete_dto(self):
        return ProductPkDto(
            article_pk = self.kwargs['pk']
        )