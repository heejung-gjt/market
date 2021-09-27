from django.urls import path
from product.views import (
    ProductView, ProductDetailView, ProductCreateView, FilterProductView,
    FilterSubProductView, ProductEditView, DeleteView, ProductSearchView, 
    ProductCategoryUploadView)
from django.conf import settings
from django.conf.urls.static import static

app_name = 'product'
urlpatterns = [
    path('', ProductView.as_view(),name='article'),
    path('detail/<pk>', ProductDetailView.as_view(),name='detail'),
    path('select/', FilterProductView.as_view(),name='select'),
    path('select/detail/', FilterSubProductView.as_view(),name='select_detail'),
    path('edit/<pk>',ProductEditView.as_view(), name='edit'),
    path('delete/<pk>',DeleteView.as_view(), name='delete'),
    path('filter/',ProductSearchView.as_view(), name='filter'),
    path('upload/category/', ProductCategoryUploadView.as_view(), name='upload_category'),
    # path('like',LikeView.as_view(), name='like'),
    #  path('user/', include('user.urls')),
    
    
    # 이미지 업로드
    path('upload/', ProductCreateView.as_view(),name='upload_product'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)