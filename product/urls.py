from django.urls import path
from product.views import (
    ProductView, ProductDetailView, ProductCreateView, FilterProductView,
    FilterSubProductView, ProductEditView, DeleteView, ProductSearchView, 
    ProductCategoryUploadView)

app_name = 'product'
urlpatterns = [
    path('', ProductView.as_view(),name='article'),
    path('detail/<pk>', ProductDetailView.as_view(),name='detail'),
    path('select/', FilterProductView.as_view(),name='select'),
    path('filter/select/', FilterSubProductView.as_view(),name='select_detail'),
    path('edit/<pk>',ProductEditView.as_view(), name='edit'),
    path('delete/<pk>',DeleteView.as_view(), name='delete'),
    path('search/',ProductSearchView.as_view(), name='filter'),
    path('upload/category/', ProductCategoryUploadView.as_view(), name='upload_category'),    
    # 이미지 업로드
    path('upload/', ProductCreateView.as_view(),name='upload_product'),
]