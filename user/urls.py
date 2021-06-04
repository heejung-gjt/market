from django.urls import path
from user.views import LoginView,LegisterView

app_name = 'user'

urlpatterns = [
  path('signin/',LoginView.as_view(), name='signin'),
  path('signup/',LegisterView.as_view(), name='signup'),
]