from django.urls import path
from user.views import LoginView

app_name = 'user'

urlpatterns = [
  path('signin/',LoginView.as_view(), name='signin'),
]