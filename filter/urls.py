from django.contrib import admin
from django.urls import path, include
from filter.views import CategoryView, CategoryListView

app_name = 'filter'
urlpatterns = [
  path('category/', CategoryView.as_view(),name='category'),
  path('category-list/<pk>', CategoryListView.as_view(),name='category-list'),
]