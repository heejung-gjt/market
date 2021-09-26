import time
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

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


# 페이징 처리 함수
def paginator(product_list, page, p):
  paginator = Paginator(product_list, p)
  try:
    article_obj = paginator.page(page)
  except PageNotAnInteger:
    article_obj = paginator.page(1)
  except EmptyPage:
    article_obj = paginator.page(paginator.num_pages)
  
  index = article_obj.number
  max_index = len(paginator.page_range)
  page_size = 5
  current_page = int(index) if index else 1
  start_index = int((current_page - 1) / page_size) * page_size
  end_index = start_index + page_size
  if end_index >= max_index:
      end_index = max_index
  page_range = paginator.page_range[start_index:end_index]
  return article_obj, page_range


