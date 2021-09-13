import time


# context 정보 넣기
def context_infor(**kwargs):
  a = {}
  for k,v in kwargs.items():
    a[k] = v
  return a


# comment 시간 나타내기
def get_time_passed(object):
    time_passed = int(float(time.time()) - float(object.created_at))
    if time_passed == 0:
        return '1초 전'
    if time_passed < 60:
        return str(time_passed) + '초 전'
    if time_passed//60 < 60:
        return str(time_passed//60) + '분 전'
    if time_passed//(60*60) < 24:
        return str(time_passed//(60*60)) + '시간 전'
    if time_passed//(60*60*24) < 30:
        return str(time_passed//(60*60*24)) + '일 전'
    if time_passed//(60*60*24*30) < 12:
        return str(time_passed//(60*60*24*30)) + '달 전'
    else:
        return '오래 전'  


# 제품 upload 시간 나타내기
def upload_get_time_passed(create_time):
    time_passed = int(float(time.time()) - float(create_time))
    if time_passed == 0:
        return '1초 전'
    if time_passed < 60:
        return str(time_passed) + '초 전'
    if time_passed//60 < 60:
        return str(time_passed//60) + '분 전'
    if time_passed//(60*60) < 24:
        return str(time_passed//(60*60)) + '시간 전'
    if time_passed//(60*60*24) < 30:
        return str(time_passed//(60*60*24)) + '일 전'
    if time_passed//(60*60*24*30) < 12:
        return str(time_passed//(60*60*24*30)) + '달 전'
    else:
        return '오래 전'  


# product sale percentage function
def calculate_price(origin_price, sale_price):
  try:
    price = sale_price
    price_gap = int(origin_price) - int(price)
    real_sale = int(price_gap)/int(origin_price)*100
    discount_rate = round(real_sale, 1)
    return discount_rate
  except:
    discount_rate = -1
    return discount_rate

