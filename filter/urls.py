from django.urls import path
from filter.views import CategoryView

app_name = 'filter'
urlpatterns = [
  path('category/list/<pk>', CategoryView.as_view(),name='category-list'),

]