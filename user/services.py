from filter.services import UserFilterService
from django.contrib import auth
from django.contrib.auth.models import User
from .models import Profile
from .dto import SignupDto, SigninDto, UpdateUserDto
from .utils import signup_error_chk, signin_error_chk, context,chk_user_profile_nickname,chk_nickname_exist


# update user profile infor 
def update_profile(**kwargs):
  user = UserFilterService.find_by_user(kwargs['user_pk'])
  if kwargs['image'] == []:
    Profile.objects.filter(user__pk=kwargs['user_pk']).update(
      user = user,
      nickname = kwargs['nickname'],
      )

  else:
    Profile.objects.filter(user__pk = kwargs['user_pk']).delete()
    Profile.objects.filter(user__pk = kwargs['user_pk']).create(
      user = user,
      image = kwargs['image'][0],
      nickname = kwargs['nickname'],
    )


# crud user infor
class UserService():

  @staticmethod
  def signup(dto:SignupDto):
    result = signup_error_chk(userid= dto.userid,nickname=dto.nickname, password=dto.password, password_chk=dto.password_chk)
    if not result['error']['state']:
      user = User.objects.create_user(username=dto.userid, password=dto.password)
      Profile.objects.create(user = user,nickname = dto.nickname,image = "감자.png")
      result = context(False,'completed',user)
    return result

  @staticmethod
  def signin(dto:SigninDto):
    user = auth.authenticate(username=dto.userid, password=dto.password)
    result = signin_error_chk(user = user)
    return result

  @staticmethod
  def update(dto:UpdateUserDto):
    if dto.nickname == '':
      result = context(True,'변경할 닉네임을 입력해주세요')
      return result

    nickname_is_exist = chk_user_profile_nickname(user_pk =dto.user_pk, nickname = dto.nickname)
    
    if nickname_is_exist:
      update_profile(user_pk = dto.user_pk, nickname=dto.nickname, image=dto.image)
      result = context(False,'completed')  
      return result

    else:
      result = chk_nickname_exist(nickname = dto.nickname)
      if not result['error']['state']:
         update_profile(user_pk = dto.user_pk, nickname=dto.nickname, image=dto.image)
    return result
    

