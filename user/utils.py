from django.contrib.auth.models import User
from .models import Profile


def context(state,msg=None,user=None):
  result = {
      'error':{
        'state':state,
        'msg':msg
      },
      'user':user
    }
  return result


# user signup utils
def signup_error_chk(**kwargs):
  user = User.objects.filter(username = kwargs['userid'])
  nickname = Profile.objects.filter(nickname = kwargs['nickname'])

  if not kwargs['userid'] or not kwargs['password'] or not kwargs['password_chk'] or not kwargs['nickname']:
      result = context(True,'모든 내용을 입력해주세요')
      return result
    
  if len(user) > 0 :
    result = context(True,'아이디가 이미 존재합니다')
    return result

  if len(nickname) > 0 :
    result = context(True,'닉네임이 이미 존재합니다')
    return result
  
  if kwargs['password'] != kwargs['password_chk']:
    result = context(True,'비밀번호가 틀립니다')
    return result

  result = context(False,'comeplted')
  return result


# user signin utils
def signin_error_chk(**kwargs):
  if kwargs['user'] is None:
    result = context(True, '아이디와 비밀번호를 확인해주세요')
    return result
  else:
    result = context(False,'comepleted',kwargs['user'])
    return result 


# user profile utils - Posts the user clicked on the like button
def find_user_liked_article(request,articles,lists):

  for article in articles.all():
    if request.user in article.like.users.all():
      lists.append(article)
  return lists


# user profile utils - Check if a user has written a post or if a user clicked like button
def check_profile_infor_empty(like_articles, user_articles):
  like_article_empty = False
  writer_article_empty=False
  if like_articles == []:
      like_article_empty = True
  if user_articles.first() == None:
      writer_article_empty = True
  return like_article_empty,writer_article_empty


# user profile utils - Check if the nickname of the current user is the same
def chk_user_profile_nickname(**kwargs):
  if Profile.objects.filter(user__pk=kwargs['user_pk']).first().nickname == kwargs['nickname']:
    is_exist = True
  else:
    is_exist = False
  return is_exist


# user profile utils - Check if the user's nickname already exists
def chk_nickname_exist(**kwargs):
  if len(Profile.objects.filter(nickname=kwargs['nickname'])) > 0:
    result = context(True,'닉네임이 이미 존재합니다')
  else:
    result = context(False,'completed')
  return result

