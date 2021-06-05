from django.urls import path
from user.views import LoginView,LegisterView,ProfileView

app_name = 'user'

urlpatterns = [
  path('signin/',LoginView.as_view(), name='signin'),
  path('signup/',LegisterView.as_view(), name='signup'),
  path('profile/',ProfileView.as_view(), name='profile'),
]