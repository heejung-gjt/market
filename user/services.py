from utils import context_infor
from django.shortcuts import get_object_or_404
from django.contrib import auth
from user.models import User, Address
from .dto import SignupDto, SigninDto, UpdateUserAddressDto, UpdateUserDto
from datetime import datetime
from market.settings import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_STORAGE_BUCKET_NAME,AWS_S3_REGION_NAME
from boto3.session import Session
from .utils import signup_error_chk, signin_error_chk, context,chk_user_profile_nickname,chk_nickname_exist


# update user profile infor 
def update_profile(**kwargs):
  if kwargs['image'] is None:
    User.objects.filter(pk=kwargs['user_pk']).update(nickname = kwargs['nickname'])
    user = User.objects.get(pk=kwargs['user_pk'])
    print(user)
    Address.objects.filter(user=user).update(address=kwargs['address'], address_detail=kwargs['address_detail'])
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
      s3.Bucket(AWS_STORAGE_BUCKET_NAME).put_object(
        Key = now+file.name,
        Body = file
      )
      s3_url = "https://django-s3-practices.s3.ap-northeast-2.amazonaws.com/"
      user = User.objects.filter(pk=kwargs['user_pk']).update(
        image = s3_url+now+file.name,
        nickname = kwargs['nickname'],
      )
      Address.objects.filter(user=user).update(address=kwargs['address'], address_detail=kwargs['address_detail'])

# crud user infor
class UserService():

    @staticmethod
    def signup(dto:SignupDto):
        if dto.address== '' or dto.address_detail== '':
            result = context(True,'주소를 입력해주세요')
            return result

        result = signup_error_chk(
            userid = dto.userid,
            nickname=dto.nickname, 
            password=dto.password, 
            password_chk=dto.password_chk
        )
        
        if not result['error']['state']:
            user = User.objects.create_user(
                email=dto.userid, 
                nickname=dto.nickname, 
                password=dto.password,
                image = "potato.png", 
                is_address=True
                )

            Address.objects.create(
                user = user,
                address = dto.address,
                address_detail = dto.address_detail,
            )
            result = context(False,'completed',user)
            return result
        return result

    @staticmethod
    def signin(dto:SigninDto):
        user = auth.authenticate(email=dto.userid, password=dto.password)
        result = signin_error_chk(user = user)
        return result

    @staticmethod
    def update(dto:UpdateUserDto):
        if dto.nickname == '':
            result = context(True,'변경할 닉네임을 입력해주세요')
            return result
        if dto.address == '' or dto.address_detail == '':
          result = context(True, '변경할 주소를 입력해주세요')
          return result
        nickname_is_exist = chk_user_profile_nickname(user_pk =dto.user_pk, nickname = dto.nickname)
        if nickname_is_exist:
            update_profile(user_pk = dto.user_pk, nickname=dto.nickname, image=dto.image, address=dto.address, address_detail=dto.address_detail)
            result = context(False,'completed')  
            return result
        else:
            result = chk_nickname_exist(nickname = dto.nickname)
        if not result['error']['state']:
            update_profile(user_pk = dto.user_pk, nickname=dto.nickname, image=dto.image, address=dto.address, address_detail=dto.address_detail)
            return result
        
    @staticmethod
    def input_address(dto:UpdateUserAddressDto):
        if not dto.user or not dto.address or not dto.address_detail:
            result = context(True, '주소를 입력해주세요 !')
            return result
        User.objects.filter(pk = dto.user).update(
            is_address = True
        )
        Address.objects.create(
            user = User.objects.filter(pk = dto.user).first(),
            address = dto.address,
            address_detail = dto.address_detail
        )
        result = context(False,'comeplted')
        return result

    @staticmethod
    def create_kakao_user(profile_request):
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
        context = context_infor(state=True, user=user)
        return context


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
    user = User.objects.filter(pk=pk).first()
    return user

  @staticmethod  
  def get_profile_infor(pk):
    result = User.objects.get(pk = pk)
    return result