from django.db import models
from behaviors import TimeStampable, Deleteable
from django.contrib.auth.models import (BaseUserManager, AbstractBaseUser, PermissionsMixin)


class UserManager(BaseUserManager):
    def _create_user(self, email, password=None, **extra_fields):

        if not email:
            raise ValueError('Users must have an email address')
        
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)
    
    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)
        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin, TimeStampable, Deleteable):
    """
    is_agreed : 사용자 정책 동의 관련 필드
    is_detailed : 사용자 부가 내용 작성 관련 필드
    """
    image = models.TextField(verbose_name=('Profile image'),)
    email = models.TextField(verbose_name=('Email Address'), max_length=255,unique=True,)
    nickname = models.CharField(verbose_name=('Nickname'), max_length=30,unique=True)
    is_active = models.BooleanField(verbose_name=('Is active'), default=True)
    is_staff = models.BooleanField(verbose_name=('Is staff'), default=False)
    is_agreed = models.BooleanField(verbose_name=('Is agreed'), default=False)
    is_detailed = models.BooleanField(verbose_name=('Is detailed'), default=False)
    is_liked = models.BooleanField(verbose_name=('Is_liked'), default=False)
    auth = models.CharField(max_length=50,blank=True,null=True)
    objects = UserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nickname']

    def __str__(self):
        return self.nickname

  


