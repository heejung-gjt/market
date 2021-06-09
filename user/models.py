from django.db import models
from behaviors import Nameable, TimeStampable, Deleteable
# Create your models here.

class User(TimeStampable, Deleteable):
  username = models.CharField(max_length=64)
  email = models.EmailField(max_length=64)
  password = models.CharField(max_length=64)

  def __str__(self):
    return self.username
  
  class Meta:
    db_table = 'users'


class Profile(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
  nickname = models.CharField(max_length=64)