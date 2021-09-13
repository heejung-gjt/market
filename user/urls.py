from os import name
from django.urls import path
from user.views import LoginView,RegisterView,ProfileView,logout, kakao_login, kakao_login_callback, SignupAddressView
from django.conf import settings
from django.conf.urls.static import static


app_name = 'user'

urlpatterns = [
  path('signin/',LoginView.as_view(), name='signin'),
  path('signup/',RegisterView.as_view(), name='signup'),
  path('logout/',logout, name='logout'),
  path('profile/<pk>',ProfileView.as_view(), name='profile'),
  path('signin/kakao/', kakao_login, name='kakao_login'),
  path('signin/kakao/callback/', kakao_login_callback, name='kakao-callback'),
  path('signup/address/', SignupAddressView.as_view(), name='kakao-address'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)