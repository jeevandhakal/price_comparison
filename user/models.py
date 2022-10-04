from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import ugettext_lazy as _
from .managers import CustomUserManager



class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class UserOTP(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    time_st = models.DateTimeField(auto_now=True)
    otp = models.SmallIntegerField()

    def __str__(self):
        return self.user.first_name

    

    

