from social.models import Like
from django.contrib.auth.models import User
from django.shortcuts import render,redirect
from django.views.generic import View
from django.http import JsonResponse
from filter.services import ProductFilterService
from product.models import Article
from user.models import Profile
from .services import UserService
from django.contrib import auth
from .dto import SignupDto,SigninDto, UpdateUserDto

import json
import bcrypt
import jwt


class LoginView(View):

  def get(self,request, *args, **kwargs):
    categorys = ProductFilterService.find_by_all_category()
    context = {'category_list':categorys}
    return render(request, 'signin.html',context)

  def post(self,request, *args, **kwargs):

    return redirect('home')


class RegisterView(View):

    def get(self,request, *args, **kwargs):
        categorys = ProductFilterService.find_by_all_category()
        context = {'category_list':categorys}
        return render(request, 'signup.html',context)

    def post(self, request):
        user_dto = self._build_user_dto(request)
        context = UserService.signup(user_dto)
        if not context['error']['state']:
            auth.login(request, context['user'])
            return redirect('product:article')
        return render(request,'signup.html',context)
    
    def _build_user_dto(self, request):
        return SignupDto(
            userid = request.POST['userid'],
            nickname = request.POST['nickname'],
            password = request.POST['password'],
            password_chk = request.POST['password_chk']
        )

  
class LoginView(View):

    def get(self, request, *args, **kwargs):
        return render(request,'signin.html')

    def post(self,request, *args, **kwargs):
        signin_dto = self._fetch_signin_dto(request.POST)
        context = UserService.signin(signin_dto)
        if context['error']['state']:
            return render(request,'signin.html',context)
        auth.login(request, context['user'])
        return redirect('product:article')

    @staticmethod
    def _fetch_signin_dto(post_data):
        return SigninDto(
        userid = post_data['userid'],
        password = post_data['password']
        )


def logout(request):
  auth.logout(request)
  return redirect('product:article')


class ProfileView(View):
    def get(self,request, *args, **kwargs):
        categorys = ProductFilterService.find_by_all_category()
        writer_articles = Article.objects.filter(is_deleted=False, writer=request.user)
        like_articles = Like.objects.filter(users__pk = request.user.pk).all()
        print('dddddddddd',like_articles)
        context = {'category_list':categorys,'articles':writer_articles,'like_articles':like_articles}
        return render(request, 'profile.html',context)
	
    def post(self,request, *args, **kwargs):
	    user_infor_dto = self._build_user_infor(request)
	    UserService.update(user_infor_dto)


	    return redirect('user:profile',kwargs['pk'])
	
    def _build_user_infor(self,request):
        return UpdateUserDto(
            image = request.FILES.getlist('image'),
            userid = request.POST['userid'],
            nickname = request.POST['nickname'],
            password = request.POST['password'],
            user_pk = request.user.pk 
        )
			
