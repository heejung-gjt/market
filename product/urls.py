from django.contrib import admin
from django.urls import path, include
from product.views import ProductView,CategoryView, DetailView

app_name = 'product'
urlpatterns = [
    path('', ProductView.as_view(),name='article'),
    path('category/', CategoryView.as_view(),name='category'),
    path('detail/', DetailView.as_view(),name='detail'),
    path('user/', include('user.urls')),
]