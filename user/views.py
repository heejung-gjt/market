from django.shortcuts import render,redirect
from django.views.generic import View
from django.contrib import auth
from social.models import Like
from product.models import Article
from filter.services import ProductFilterService
from .services import UserService
from .dto import SignupDto,SigninDto, UpdateUserDto


def nav_sub_menu_categories():
    sub_menu_categories = ProductFilterService.find_by_all_category()
    context = {'category_list':sub_menu_categories}
    return context


# 회원가입 
class RegisterView(View):

    def get(self,request, *args, **kwargs):
        context = nav_sub_menu_categories()
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


# 로그인
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


def logout(request):
  auth.logout(request)
  return redirect('product:article')


class ProfileView(View):
    def get(self,request, *args, **kwargs):
        categorys = ProductFilterService.find_by_all_category()
        writer_articles = Article.objects.filter(is_deleted=False, writer=request.user)
        like_articles = Like.objects.filter(users__pk = request.user.pk).all()
        articles = Article.objects.filter(is_deleted=False).all()
        like_articles = []
        
        for article in articles:
            if request.user in article.like.users.all():
                like_articles.append(article)
        context = {'category_list':categorys,'articles':writer_articles,'like_articles':like_articles}

        if like_articles == []:
            context['empty'] = True
        if writer_articles.first() == None:
            context['writer_empty'] = True
        return render(request, 'profile.html',context)
	
    def post(self,request, *args, **kwargs):
	    user_infor_dto = self._build_user_infor(request)
	    UserService.update(user_infor_dto)


	    return redirect('user:profile',kwargs['pk'])
	
    def _build_user_infor(self,request):
        return UpdateUserDto(
            image = request.FILES.getlist('image'),
            nickname = request.POST['nickname'],
            user_pk = request.user.pk 
        )
			
