from django.urls import path
from product.views import ProductView,DetailView,ArticleCreateView,SelectView,SelectDetailView,EditView,DeleteView
from product import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'product'
urlpatterns = [
    path('', ProductView.as_view(),name='article'),
    path('detail/<pk>', DetailView.as_view(),name='detail'),
    path('select/', SelectView.as_view(),name='select'),
    path('select/detail/', SelectDetailView.as_view(),name='select_detail'),
    path('edit/<pk>',EditView.as_view(), name='edit'),
    path('delete/<pk>',DeleteView.as_view(), name='delete'),
    # path('like',LikeView.as_view(), name='like'),
    #  path('user/', include('user.urls')),
    
    
    # 이미지 업로드
    path('upload_product/', ArticleCreateView.as_view(),name='upload_product'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)