from django.urls import path
from user.views import LoginView,RegisterView,ProfileView,logout
from django.conf import settings
from django.conf.urls.static import static


app_name = 'user'

urlpatterns = [
  path('signin/',LoginView.as_view(), name='signin'),
  path('signup/',RegisterView.as_view(), name='signup'),
  path('logout/',logout, name='logout'),
  path('profile/<pk>',ProfileView.as_view(), name='profile'),
  
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)