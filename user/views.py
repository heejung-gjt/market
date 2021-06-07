from django.shortcuts import render,redirect
from django.views.generic import View
from django.views.generic import TemplateView
from filter.services import ProductFilterService
# Create your views here.


class LoginView(View):

  def get(self,request, *args, **kwargs):
    categorys = ProductFilterService.find_by_all_category()
    context = {'category_list':categorys}
    return render(request, 'signin.html',context)

  def post(self,request, *args, **kwargs):

    return redirect('home')


class LegisterView(View):

  def get(self,request, *args, **kwargs):
    categorys = ProductFilterService.find_by_all_category()
    context = {'category_list':categorys}
    return render(request, 'signup.html',context)

  def post(self,request, *args, **kwargs):
    
    return redirect('home')


class ProfileView(View):
   def get(self,request, *args, **kwargs):
    categorys = ProductFilterService.find_by_all_category()
    writer_articles = ProductFilterService.find_by_filter_article(request.user)
    context = {'category_list':categorys,'articles':writer_articles}
    return render(request, 'profile.html',context)