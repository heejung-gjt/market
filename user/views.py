from django.shortcuts import render,redirect
from utils import context_infor
from django.contrib import auth
from django.views.generic import View
from .services import UserService
from filter.services import ProductFilterService
from .dto import KakaoUserInforDto, SignupDto,SigninDto, UpdateUserAddressDto, UpdateUserDto
from .utils import find_user_liked_article,check_profile_infor_empty
from .exception import KakaoException

import requests
import os


# KakaoLoginCallback class에 kakao 프로필 정보 반환하는 메서드
def get_profile_infor(data):
    request_access_token = requests.get(
        f"https://kauth.kakao.com/oauth/token?grant_type=authorization_code&client_id={data.client_id}&redirect_uri={data.redirect_uri}&code={data.code}&client_secret={data.client_secret}",
        headers={"Accept": "application/json"},
        )
    token_info_json = request_access_token.json()
    error = token_info_json.get("error", None)
    if error is not None:
        raise KakaoException()
    access_token = token_info_json.get("access_token")
    headers = {"Authorization": f"Bearer {access_token}"}
    profile_request = requests.get("https://kapi.kakao.com/v2/user/me", headers=headers)    
    return profile_request


# sub menu category list
def nav_sub_menu_categories():
    sub_menu_categories = ProductFilterService.find_by_all_category()
    context = context_infor(category_list = sub_menu_categories)
    return context


class RegisterView(View):

    def get(self,request, *args, **kwargs):
        context = nav_sub_menu_categories()
        return render(request, 'signup.html',context)

    def post(self, request):
        data = self._build_user_dto(request.POST)
        context = UserService.signup(data)
        if not context['error']['state']:
            auth.login(request, context['user'])
            return redirect('product:article')
        return render(request,'signup.html',context)
    
    @staticmethod
    def _build_user_dto(post_data):
        return SignupDto(
            userid = post_data['userid'],
            nickname = post_data['nickname'],
            password = post_data['password'],
            password_chk = post_data['password_chk'],
            address = post_data['address'],
            address_detail = post_data['address-detail']
        )


class LoginView(View):

    def get(self, request, *args, **kwargs):
        context = nav_sub_menu_categories()
        return render(request,'signin.html',context)

    def post(self, request, *args, **kwargs):
        signin_dto = self._build_signin_dto(request.POST)
        context = UserService.signin(signin_dto)
        if context['error']['state']:
            return render(request,'signin.html',context)
        auth.login(request, context['user'])
        return redirect('product:article')

    @staticmethod
    def _build_signin_dto(post_data):
        return SigninDto(
        userid = post_data['userid'],
        password = post_data['password']
        )


# social login kakao
class KakaoLoginView(View):

    def get(self, request, *args, **kwargs):
        data = self._build_kakao_dto()
        CLIENT_ID = data.client_id
        REDIRECT_URI = data.redirect_uri
        return redirect(f"https://kauth.kakao.com/oauth/authorize?client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}&response_type=code")

    @staticmethod
    def _build_kakao_dto():
        return KakaoUserInforDto(
            client_id = os.environ.get('KAKAO_ID'),
            redirect_uri = "http://gamjamarket.site/user/signin/kakao/callback",
            code = None,
            client_uri = None,
            client_secret = None
        )


class KakaoLoginCallBackView(View):
    
    def get(self,request, *args, **kwargs):
        try:
            data = self._build_kakao_dto(request)
            profile_request = get_profile_infor(data) # get profile data
            result = UserService.create_kakao_user(profile_request)
            if result['state']:
                user = result['user']
                auth.login(request, user)
                if user.is_address == False:
                    return redirect('user:kakao-address')
                return redirect("/")
        except KakaoException:
            raise("can't get data")
    
    def _build_kakao_dto(self, request):
        return KakaoUserInforDto(
            client_id = os.environ.get('KAKAO_ID'),
            redirect_uri = "http://gamjamarket.site/user/signin/kakao/callback",
            code = request.GET.get('code', None),
            client_uri = None,
            client_secret = os.environ.get('SECRET_KEY')
        )


# kakao 첫 로그인시 주소 입력받는 class 
class SignupAddressView(View):

    def get(self, request, *args, **kwargs):
        sub_menu_categories = ProductFilterService.find_by_all_category()
        context = context_infor(category_list = sub_menu_categories)
        return render(request, 'kakao-address.html', context)
        
    def post(self, request, *args, **kwargs):
        address_dto = self._build_address_dto(request)
        context = UserService.input_address(address_dto)
        if context['error']['state']:
            return render(request, 'kakao-address.html', context)
        return redirect('/')
    
    def _build_address_dto(self, request): # user의 pk를 받아야 하기 때문에 @staticmethod사용할 수 없음
        return UpdateUserAddressDto(
            user = request.user.pk,
            address = request.POST['address'],
            address_detail = request.POST['address-detail']
        )


def logout(request):
  auth.logout(request)
  return redirect('product:article')


class ProfileView(View):

    def get(self,request, *args, **kwargs):
        categories = ProductFilterService.find_by_all_category()
        user_articles = ProductFilterService.find_not_deleted_user_article_list(is_deleted=False, writer=request.user)
        articles = ProductFilterService.find_by_not_deleted_article()
        liked_article_list = find_user_liked_article(request,articles,[])
        like_empty, writer_empty = check_profile_infor_empty(liked_article_list,user_articles)
        context = context_infor(
            category_list = categories,
            articles = user_articles, 
            like_articles = liked_article_list, 
            empty = like_empty, 
            writer_empty = writer_empty
            )
        return render(request, 'profile.html',context)
	
    def post(self,request, *args, **kwargs):
        profile_pk = kwargs['pk']
        user_infor_dto = self._build_user_infor(request)
        result = UserService.update(user_infor_dto)
        if result['error']['state']:
            categories = ProductFilterService.find_by_all_category()
            context = context_infor(state = True, msg = result['error']['msg'], category_list = categories)
            return render(request,'profile.html',context)
        return redirect('user:profile',profile_pk)
	
    def _build_user_infor(self,request):
        return UpdateUserDto(
            image = request.FILES.get('image'),
            nickname = request.POST['nickname'],
            address = request.POST['address'],
            address_detail = request.POST['address_detail'],
            user_pk = request.user.pk 
        )
			
