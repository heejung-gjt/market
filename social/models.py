from django.db import models
from behaviors import Nameable, TimeStampable
from django.contrib.auth.models import User
from product.models import Article


class Comment(Nameable, TimeStampable):
    writer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='guest_comment')
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='comment')
    
    def __str__(self):
        return self.name


class Like(models.Model):
  comment = models.OneToOneField(Article, on_delete=models.CASCADE, related_name='like')
  users = models.ManyToManyField(User, related_name='like',blank=True)

  def __str__(self):
    return self.comment.content   