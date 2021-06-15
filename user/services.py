from django.contrib import auth
from django.contrib.auth.models import User
from .models import Profile
from .dto import SignupDto, SigninDto, UpdateUserDto
from .utils import signup_error_chk, signin_error_chk, context


class UserService():

  @staticmethod
  def signup(dto:SignupDto):

    result = signup_error_chk(userid= dto.userid,nickname=dto.nickname, password=dto.password, password_chk=dto.password_chk)
    
    if not result['error']['state']:
      user = User.objects.create_user(username=dto.userid, password=dto.password)
      Profile.objects.create(
        user = user,
        nickname = dto.nickname,
        image = "감자.png"
      )
      result = context(False,'completed',user)
    return result

  @staticmethod
  def signin(dto:SigninDto):
    user = auth.authenticate(username=dto.userid, password=dto.password)
    result = signin_error_chk(user = user)
    return result

  @staticmethod
  def update(dto:UpdateUserDto):
    result ={
    'error':{
      'state':False,
      'msg':'',
    },
  }
    user = User.objects.filter(pk=dto.user_pk).first()
    
    Profile.objects.filter(user__pk =dto.user_pk).delete()
    Profile.objects.filter(user__pk=dto.user_pk).create(
      user = user,
      image = dto.image[0],
      nickname = dto.nickname,
    )




