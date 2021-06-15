
def context(state,msg=None,user=None):
  result = {
      'error':{
        'state':state,
        'msg':msg
      },
      'user':user
    }
  return result


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


def signin_error_chk(**kwargs):
  if kwargs['user'] is None:
    result = context(True, '아이디와 비밀번호를 확인해주세요')
    return result
  else:
    result = context(False,'comepleted',kwargs['user'])
    return result 
