from django.db import models
from behaviors import TimeStampable
from user.models import User
from product.models import Article

import time


class Comment(TimeStampable):
    content = models.CharField(max_length=255)
    article = models.ForeignKey(Article, on_delete=models.SET_NULL, null=True, related_name='comment')
    writer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='guest_comment')
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='comment')

    @property
    def created_string(self):
      time_passed = int(float(time.time()) - float(self.created_at))
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

    def __str__(self):
        return self.content


class ReComment(TimeStampable):
  content = models.CharField(max_length=255)
  writer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='re_comment')
  comment = models.ManyToManyField(Comment, related_name='re_comment',blank=True)

  @property
  def created_string(self):
    time_passed = int(float(time.time()) - float(self.created_at))
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

class Like(models.Model):
  article = models.OneToOneField(Article, on_delete=models.CASCADE, related_name='like')
  users = models.ManyToManyField(User, related_name='like',blank=True)
  is_liked = models.BooleanField(default=False)
   
