from django.shortcuts import get_object_or_404
from django.contrib import auth
from user.models import User
from .dto import SignupDto, SigninDto, UpdateUserDto
from datetime import datetime
from market.settings import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_STORAGE_BUCKET_NAME,AWS_S3_REGION_NAME
from boto3.session import Session
from .utils import signup_error_chk, signin_error_chk, context,chk_user_profile_nickname,chk_nickname_exist


# update user profile infor 
def update_profile(**kwargs):
  print('여기로 오기ㄹ는 함',kwargs['user_pk'])

  if kwargs['image'] is None:
    User.objects.filter(pk=kwargs['user_pk']).update(
      nickname = kwargs['nickname'],
      )

  else:
    file = kwargs['image']
    if file is not None:
      session = Session(
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        region_name=AWS_S3_REGION_NAME
      )
      s3 = session.resource('s3')
      now = datetime.now().strftime('%Y%H%M%S')
      img_object = s3.Bucket(AWS_STORAGE_BUCKET_NAME).put_object(
        Key = now+file.name,
        Body = file
      )
      # 환경변수로 빼준다
      s3_url = "https://django-s3-practices.s3.ap-northeast-2.amazonaws.com/"
      User.objects.filter(pk=kwargs['user_pk']).update(
        image = s3_url+now+file.name,
        nickname = kwargs['nickname']
      )



# crud user infor
class UserService():

  @staticmethod
  def signup(dto:SignupDto):
    result = signup_error_chk(userid= dto.userid,nickname=dto.nickname, password=dto.password, password_chk=dto.password_chk)
    if not result['error']['state']:
      user = User.objects.create_user(email=dto.userid, nickname=dto.nickname, password=dto.password,image = "감자.png")
      result = context(False,'completed',user)
    return result

  @staticmethod
  def signin(dto:SigninDto):
    user = auth.authenticate(email=dto.userid, password=dto.password)
    result = signin_error_chk(user = user)
    return result

  @staticmethod
  def update(dto:UpdateUserDto):
    print('dto 유저 pk',dto.user_pk)
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
    

class UserFilterService():

  @staticmethod
  def find_user_infor(pk):
    result = get_object_or_404(User, pk = pk) 
    return result

  @staticmethod
  def find_profile_infor(pk):
    result = get_object_or_404(User, pk = pk)
    return result 

  @staticmethod
  def find_by_user(pk):
    print('접근은함')
    user = User.objects.filter(pk=pk).first()
    return user

  @staticmethod  
  def get_profile_infor(pk):
    result = User.objects.get(pk = pk)
    return result