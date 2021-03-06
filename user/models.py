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

    image = models.TextField(verbose_name=('Profile image'))
    email = models.EmailField(verbose_name=('Email address'), max_length=255,unique=True,)
    nickname = models.CharField(verbose_name=('Nickname'), max_length=30, unique=True)
    is_active = models.BooleanField(verbose_name=('Is active'), default=True)
    is_staff = models.BooleanField(verbose_name=('Is staff'), default=False)
    is_address = models.BooleanField(verbose_name=('Is address'), default=False)    
    objects = UserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nickname']

    def __str__(self):
        return self.nickname


class Address(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True,  related_name='address')
    address = models.TextField()
    address_detail = models.TextField()
    
    def __str__(self):
        return self.address

