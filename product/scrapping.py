import requests
from bs4 import BeautifulSoup
import sys
import time
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)) + '/app')))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "market.settings")
import django
django.setup()
from datetime import datetime
from product.models import Article, Price
from filter.models import CategoryDetail
from utils import calculate_price
from user.models import User
from social.models import Like






def dict_infor(**kwargs):
  context = {}
  for k,v in kwargs.items():
      context[k] = v
  return context

def scrapping():
  data_list = []

  response = requests.get(f'https://www.daangn.com/hot_articles')
  soup = BeautifulSoup(response.text, 'html.parser')

  # 메인 페이지 기사 ul
  sections = soup.select_one('#content > section.cards-wrap')
  # 메인 페이지 기사리스트들 li
  articles = sections.select('article')
  for article in articles:
        image = None
      # try:
        href = article.select_one('a')['href']
        href = f'https://www.daangn.com/{href}' 
        print(f'https://www.daangn.com/{href}')
        url = requests.get(href)
        html_each = BeautifulSoup(url.text, 'html.parser')
        content = html_each.select_one('#content')
        user = content.select_one('#nickname').text
        user_img = content.select_one('#article-profile-image > img')['src']
        print('useruser',user, user_img)
        try:
          price = content.select_one('#article-price').text.replace('\n','').replace('원','').replace(',','').strip()
        except:
          price = 0
        if price == '가격없음':
          price = 0
        print(price)
        price = int(price)
        print(price)
        origin_price = price *2
        title = content.select_one('#content > h1').text
#             category = content.select_one('.#article-category').text
        print(title)
        try:
          image = content.select_one('a > div > div > img')['data-lazy']
          print(image)
#       except:    print(category)
        except:
          pass
        category = content.select_one('#article-category').text.replace('\n','').split('∙')[0].strip()
        date = content.select_one('#article-category').text.replace('\n','').split('∙')[1].strip()
        print(category, date)
        contents = content.select_one('#article-detail').text
        print(category)
    # except:
    #     pass
        context = {'title':title,'category':category,'image':image, 'date':date, 'category_detail' : category, 'content':contents, 'origin_price':origin_price, 'price':price, 'writer':user, 'user_img': user_img}
        print(context)
        data_list.append(context)  
        print('리스트 for문',data_list)
  print()
  print()
  print(data_list)
  return data_list 

if __name__=='__main__':
    news_list = scrapping()
    print('스크래핑 성공쓰',news_list)
    i = 0
    for news in news_list:
      try:
        print('엥')
        print(news['writer'])
        user = User.objects.create(
          email = f"{news['writer']}@naver.com",
          nickname = news['writer'],
          image = news['user_img'],
          # profile_img = news['']
        )
      except:
        pass
      try:   
        category = CategoryDetail.objects.filter(name = news['category_detail']).first().category
        print(category)
      except:
        pass
      # try:
      article = Article.objects.create(
        name = news['title'],
        category = category,
        content = news['content'],
        origin_price = news['origin_price'],
        price = news['price'],
        writer = User.objects.filter(nickname = news['writer']).first(),          
        image = news['image'],
        created_at = news['date']
      )
      article.category_detail.add(CategoryDetail.objects.filter(name=news['category_detail']).first())

      Like.objects.create(
        article = article,
        is_liked = False
      )
      discount_rate = calculate_price(news['origin_price'], news['price'])
      Price.objects.create(
      article = article,
      discount_rate = discount_rate 
    )
        # except:
        #   pass
      # except:
      #   pass
