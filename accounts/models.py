from django.db import models
from django.contrib.auth.models import BaseUserManager , AbstractBaseUser
import pycountry

class MyaccountManager(BaseUserManager):
     def create_user(self,first_name,last_name,username,country,email,password= None):
          if not email:
               raise ValueError('User must have email address')
          if not username:
               raise ValueError('User must have username ')
          user = self.model(
               email = self.normalize_email(email),
               first_name = first_name,
               last_name = last_name,
               country = country,
               username = username
          )
          user.set_password(password)
          user.save(using=self._db)
          return user
     
     def create_superuser(self,first_name,country,last_name,email,username,password=None):
          user = self.create_user(
               email = self.normalize_email(email),
               first_name = first_name,
               last_name = last_name,
               username = username,
               country = country)
          

          user.set_password(password)
          user.is_admin = True
          user.is_staff = True
          user.is_active = True
          user.save(using =self._db)
          return user 
     

class account(AbstractBaseUser):
     @staticmethod
     def get_country():
          countries = list(pycountry.countries)
          country = [(country.alpha_2,country.name) for country in countries]
          return country
     
     first_name = models.CharField(max_length = 20)
     last_name = models.CharField(max_length = 15)
     email = models.EmailField(max_length = 30, unique = True)
     username = models.CharField(max_length = 50, unique = True)
     phone_number = models.CharField(max_length = 50)
     country = models.CharField(max_length = 30, choices = get_country(),default = 'US')
     date_joint = models.DateField(auto_now_add = True)
     last_joint = models.DateField(auto_now_add = True)
     is_active = models.BooleanField(default = False)
     is_admin = models.BooleanField(default = False)
     is_staff = models.BooleanField(default = False)
     is_superadmin = models.BooleanField(default = False)

     objects = MyaccountManager()
     USERNAME_FIELD = 'email'
     REQUIRED_FIELDS = ['first_name','last_name','username','country']
     def __str__(self):
          return self.email
     def has_perm(self,perm,obj=None):
          return self.is_admin
     def has_module_perms(self, app_label):
        return True 
     
