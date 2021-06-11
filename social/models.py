from django.db import models
from behaviors import Nameable, TimeStampable
from django.contrib.auth.models import User
from product.models import Article

class ReComment(TimeStampable):
  content = models.CharField(max_length=255)


class Comment(Nameable, TimeStampable):
    article = models.ForeignKey(Article, on_delete=models.SET_NULL, null=True, related_name='comment')
    writer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='guest_comment')
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='comment')
    recomment = models.ManyToManyField(ReComment, related_name='comment',blank=True)

    def __str__(self):
        return self.name


class Like(models.Model):
  article = models.OneToOneField(Article, on_delete=models.CASCADE, related_name='like')
  users = models.ManyToManyField(User, related_name='like',blank=True)
  is_liked = models.BooleanField(default=False)
   
