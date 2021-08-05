from django.shortcuts import render,redirect
from django.views.generic import View
from django.contrib import auth
from filter.services import ProductFilterService
from .services import UserService
from .dto import SignupDto,SigninDto, UpdateUserDto
from .utils import find_user_liked_article,check_profile_infor_empty

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
            password_chk = request.POST['password_chk']
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
			
