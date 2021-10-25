# sample 스크래핑 데이터

import requests
import sys
import time
import os
import django
from bs4 import BeautifulSoup
from product.models import Article, Price
from filter.models import CategoryDetail
from utils import calculate_price
from user.models import User
from social.models import Like

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)) + '/app')))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "market.settings")
django.setup()






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
        url = requests.get(href)
        html_each = BeautifulSoup(url.text, 'html.parser')
        content = html_each.select_one('#content')
        user = content.select_one('#nickname').text
        user_img = content.select_one('#article-profile-image > img')['src']
        try:
          price = content.select_one('#article-price').text.replace('\n','').replace('원','').replace(',','').strip()
        except:
          price = 0
        if price == '가격없음':
          price = 0
        price = int(price)
        origin_price = price *2
        title = content.select_one('#content > h1').text
        try:
          image = content.select_one('a > div > div > img')['data-lazy']
        except:
          pass
        category = content.select_one('#article-category').text.replace('\n','').split('∙')[0].strip()
        date = content.select_one('#article-category').text.replace('\n','').split('∙')[1].strip()
        contents = content.select_one('#article-detail').text
        context = {'title':title,'category':category,'image':image, 'date':date, 'category_detail' : category, 'content':contents, 'origin_price':origin_price, 'price':price, 'writer':user, 'user_img': user_img}
        data_list.append(context)  
  return data_list 

if __name__=='__main__':
    news_list = scrapping()
    i = 0
    for news in news_list:
      try:
        user = User.objects.create(
          email = f"{news['writer']}@naver.com",
          nickname = news['writer'],
          image = news['user_img'],
        )
      except:
        pass
      try:   
        category = CategoryDetail.objects.filter(name = news['category_detail']).first().category
      except:
        pass
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
