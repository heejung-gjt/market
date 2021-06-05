from django.shortcuts import render,redirect
from django.views.generic import View
from django.views.generic import TemplateView
# Create your views here.


class LoginView(View):

  def get(self,request, *args, **kwargs):
    return render(request, 'signin.html')

  def post(self,request, *args, **kwargs):
    
    return redirect('home')


class LegisterView(View):

  def get(self,request, *args, **kwargs):
    return render(request, 'signup.html')

  def post(self,request, *args, **kwargs):
    
    return redirect('home')


class ProfileView(TemplateView):
  template_name = 'profile.html'