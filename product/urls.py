from django.contrib import admin
from django.urls import path, include
from product.views import ProductView,DetailView,ArticleCreateView,SelectView,EditView,DeleteView
from product import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'product'
urlpatterns = [
    path('', ProductView.as_view(),name='article'),
    path('detail/<pk>', DetailView.as_view(),name='detail'),
    path('select/', SelectView.as_view(),name='select'),
    path('edit/<pk>',EditView.as_view(), name='edit'),
    path('delete/<pk>',DeleteView.as_view(), name='delete'),
    #  path('user/', include('user.urls')),
    
    
    # 이미지 업로드
    path('upload_product/', ArticleCreateView.as_view(),name='upload_product'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)