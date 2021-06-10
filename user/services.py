from django.contrib import auth
from django.contrib.auth.models import User
from .models import Profile
from .dto import SignupDto, SigninDto

class UserService():

  @staticmethod
  def signup(dto:SignupDto):
    result = {
      'error':{
        'state':False,
        'msg':''
      },
      'user':''
    }
    user = User.objects.filter(username = dto.userid)
    nickname = Profile.objects.filter(nickname = dto.nickname)
    if not dto.userid or not dto.password or not dto.password_chk or not dto.nickname:
      result['error']['state'] = True
      result['error']['msg'] = '모든 내용을 입력해주세요'
      return result
    
    if len(user) > 0 :
      result['error']['state'] = True
      result['error']['msg'] = '아이디가 이미 존재합니다'
      return result

    if len(nickname) > 0 :
      result['error']['state'] = True
      result['error']['msg'] = '닉네임이 이미 존재합니다'
      return result
    
    if dto.password != dto.password_chk:
      result['error']['state'] = True
      result['error']['msg'] = '비밀번호가 틀립니다'
      return result
    
    if not result['error']['state']:
      user = User.objects.create_user(username=dto.userid, password=dto.password)
      Profile.objects.create(
        user = user,
        nickname = dto.nickname,
      )
      result['user'] = user
      return result

  @staticmethod
  def signin(dto:SigninDto):
    result ={
    'error':{
      'state':False,
      'msg':'',
    },
    'user':''
  }
    user = auth.authenticate(username=dto.userid, password=dto.password)

    if user is None:
      result['error']['state'] = True
      result['error']['msg'] = '아이디와 비밀번호를 확인해주세요'
      return result
    result['user'] = user
    return result  
