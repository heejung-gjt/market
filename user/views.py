from django.shortcuts import render,redirect
from django.views.generic import View
from .models import User, Address
from django.contrib import auth
from filter.services import ProductFilterService
from .services import UserService
from .dto import SignupDto,SigninDto, UpdateUserDto
from .utils import find_user_liked_article,check_profile_infor_empty
import requests
from .exception import KakaoException
import os

# sub menu category list
def nav_sub_menu_categories():
    sub_menu_categories = ProductFilterService.find_by_all_category()
    context = {'category_list':sub_menu_categories}
    return context


# register
class RegisterView(View):

    def get(self,request, *args, **kwargs):
        context = nav_sub_menu_categories()
        return render(request, 'signup.html',context)

    def post(self, request):
        user_dto = self._build_user_dto(request)
        context = UserService.signup(user_dto)
        print(context)
        if not context['error']['state']:
            auth.login(request, context['user'])
            return redirect('product:article')
        return render(request,'signup.html',context)
    
    def _build_user_dto(self, request):
        return SignupDto(
            userid = request.POST['userid'],
            nickname = request.POST['nickname'],
            password = request.POST['password'],
            password_chk = request.POST['password_chk'],
            address = request.POST['address'],
            address_detail = request.POST['address-detail']
        )


# login
class LoginView(View):

    def get(self, request, *args, **kwargs):
        context = nav_sub_menu_categories()
        return render(request,'signin.html',context)

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


# social login kakao
def kakao_login(request):
    client_id = os.environ.get("KAKAO_ID")
    REDIRECT_URI = "http://127.0.0.1:8000/user/signin/kakao/callback"
    return redirect(f"https://kauth.kakao.com/oauth/authorize?client_id={client_id}&redirect_uri={REDIRECT_URI}&response_type=code")


def kakao_login_callback(request):
    code = request.GET.get('code', None)
    if code is None:
        KakaoException("Can't get code")
    client_id = os.environ.get("KAKAO_ID")
    REDIRECT_URI = "http://127.0.0.1:8000/user/signin/kakao/callback"
    client_secret = os.environ.get('SECRET_KEY')
    request_access_token = requests.get(
            f"https://kauth.kakao.com/oauth/token?grant_type=authorization_code&client_id={client_id}&redirect_uri={REDIRECT_URI}&code={code}&client_secret={client_secret}",
            headers={"Accept": "application/json"},
        )
    token_info_json = request_access_token.json()
    error = token_info_json.get("error", None)
    if error is not None:
        raise KakaoException()
    
    access_token = token_info_json.get("access_token")
    headers = {"Authorization": f"Bearer {access_token}"}
    profile_request = requests.get(
        "https://kapi.kakao.com/v2/user/me",
        headers=headers,
    )
    profile_json = profile_request.json()
    kakao_account = profile_json.get("kakao_account")
    profile = kakao_account.get("profile")
    nickname = profile.get("nickname", None)
    email = kakao_account.get("email", None)
    user, created = User.objects.get_or_create(email=email)
    if created:
        user.set_password(None)
        user.nickname = nickname
        user.is_active = True
        user.save()
        auth.login(request, user)
        if user.is_address == False:
            return redirect('user:kakao-address')
        return redirect("/")
    
    auth.login(request, user)
    if user.is_address == False:
        return redirect('user:kakao-address')
    return redirect("/")


class SignupAddressView(View):
    def get(self, request, **kwargs):
        print('여기에 도착은 합니다')
        return render(request, 'kakao-address.html')
        
    def post(self, request, **kwargs):
        print('카카오톡으로 회원가입 한 사람들의 주소 데이터가 여기로 옵니다')
        address = request.POST['address']
        address_detail = request.POST['address-detail']
        user_pk = request.user.pk
        user = User.objects.filter(pk = request.user.pk).update(
            is_address = True
        )
        Address.objects.create(
            user = User.objects.filter(pk = user_pk).first(),
            address = address,
            address_detail = address_detail
        )
        return redirect('/')


# logout
def logout(request):
  auth.logout(request)
  return redirect('product:article')


# user profile 
class ProfileView(View):

    def get(self,request, *args, **kwargs):
        categories = ProductFilterService.find_by_all_category()
        user_articles = ProductFilterService.find_not_deleted_user_article_list(is_deleted=False, writer=request.user)
        articles = ProductFilterService.find_by_not_deleted_article()
        liked_article_list = find_user_liked_article(request,articles,[])
        like_empty, writer_empty = check_profile_infor_empty(liked_article_list,user_articles)
        context = {'category_list':categories,'articles':user_articles,'like_articles':liked_article_list,'empty':like_empty,'writer_empty':writer_empty}
        return render(request, 'profile.html',context)
	
    def post(self,request, *args, **kwargs):
        profile_pk = kwargs['pk']
        user_infor_dto = self._build_user_infor(request)
        result = UserService.update(user_infor_dto)
        if result['error']['state']:
            categories = ProductFilterService.find_by_all_category()
            context = {'state':True, 'msg':result['error']['msg'],'category_list':categories}
            return render(request,'profile.html',context)

        return redirect('user:profile',profile_pk)
	
    def _build_user_infor(self,request):
        return UpdateUserDto(
            image = request.FILES.get('image'),
            nickname = request.POST['nickname'],
            user_pk = request.user.pk 
        )
			
