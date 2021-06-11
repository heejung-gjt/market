from django.db import models
from behaviors import TimeStampable, Deleteable
from django.contrib.auth.models import User
# Create your models here.


class Profile(TimeStampable, Deleteable):
  user = models.OneToOneField(User, on_delete=models.CASCADE,related_name='profile')
  nickname = models.CharField(max_length=62)
  image = models.ImageField(upload_to='image/', null=True)

  def __str__(self):
    return self.nickname
  


