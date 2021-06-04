from django.shortcuts import render,redirect
from django.views.generic import View
from django.views.generic import TemplateView
# Create your views here.


class HomeView(TemplateView):
  template_name = 'home.html'

class LoginView(View):
  
  def get(self,request, *args, **kwargs):
    return render(request, 'signin.html')

  def post(self,request, *args, **kwargs):
    
    return redirect('home')

