from django.urls import path
from user.views import LoginView,RegisterView,ProfileView,logout

app_name = 'user'

urlpatterns = [
  path('signin/',LoginView.as_view(), name='signin'),
  path('signup/',RegisterView.as_view(), name='signup'),
  path('logout/',logout, name='logout'),
  path('profile/',ProfileView.as_view(), name='profile'),
  
]