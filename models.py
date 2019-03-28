from __future__ import unicode_literals

from django.db import models, transaction
from datetime import date
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import (
    AbstractBaseUser, PermissionsMixin,
    UserManager, BaseUserManager, User)


# class Register(models.Model):
#     username=models.CharField(max_length=20)
#     email=models.EmailField(max_length=30)
#     password=models.CharField(max_length=20)
#     confirm_password=models.CharField(max_length=20)
#
#     def __str__(self):
#         return self.username

class profile(models.Model):
    user_id=models.ForeignKey(User,related_name='user_id', default='', on_delete=models.CASCADE)
    firstname=models.CharField(max_length=20)
    lastname=models.CharField(max_length=20)
    birthday=models.DateField(default=date.today)
    bloodgroup=models.CharField(max_length=10)
    photo=models.FileField(upload_to='media', default=None)
    phonenumber=models.CharField(max_length=10, default=None)


class FollowingUsers(models.Model):
	following_name=models.CharField(max_length=20)
	user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='user')



# class User(AbstractBaseUser, PermissionsMixin):
#     email = models.EmailField(max_length=40, unique=True)
#     first_name = models.CharField(max_length=30, blank=True)
#     last_name = models.CharField(max_length=30, blank=True)
#     is_active = models.BooleanField(default=True)
#     is_staff = models.BooleanField(default=False)
#     date_joined = models.DateTimeField(default=timezone.now)
#
#     objects = UserManager()
#
#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = ['first_name', 'last_name']
#
#     def save(self, *args, **kwargs):
#         super(User, self).save(*args, **kwargs)
#         return self
#
#
#
#
#
# class UserManager(BaseUserManager):
#
#     def _create_user(self, email, password, **extra_fields):
#         """
#         Creates and saves a User with the given email,and password.
#         """
#         if not email:
#             raise ValueError('The given email must be set')
#         try:
#             with transaction.atomic():
#                 user = self.model(email=email, **extra_fields)
#                 user.set_password(password)
#                 user.save(using=self._db)
#                 return user
#         except:
#             raise
#
#     def create_user(self, email, password=None, **extra_fields):
#         extra_fields.setdefault('is_staff', False)
#         extra_fields.setdefault('is_superuser', False)
#         return self._create_user(email, password, **extra_fields)
#
#     def create_superuser(self, email, password, **extra_fields):
#         extra_fields.setdefault('is_staff', True)
#         extra_fields.setdefault('is_superuser', True)
#
#         return self._create_user(email, password=password, **extra_fields)

class Wish_list(models.Model):
    user_id = models.ForeignKey(User,default='', on_delete=models.CASCADE)
    item_name=models.CharField(max_length=50)
    img_name=models.FileField(upload_to='media',default=None)
    def __str__(self):
        return self.item_name

class Category(models.Model):
    cat_name=models.CharField(max_length=100)
    def __str__(self):
        return self.cat_name

class SubCategory(models.Model):
    cat_id = models.ForeignKey(Category, on_delete=models.CASCADE, default=None)
    subcat_name=models.CharField( max_length=100)
    def __str__(self):
        return self.subcat_name

class Product(models.Model):
    subcat_id = models.ForeignKey(SubCategory,on_delete=models.CASCADE,default=None)
    item_name=models.CharField(max_length=100)
    img_name = models.FileField(upload_to='media', default=None)
    def __str__(self):
        return self.item_name