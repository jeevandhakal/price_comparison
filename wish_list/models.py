from django.db import models
from django.contrib.auth import get_user_model
from enum import Enum

User = get_user_model()

class Site(Enum):
    daraz = 1
    sastodeal = 2
    dealayo = 3


class WishList(models.Model):
    site = models.IntegerField(
        choices=((_.value, _.name) for _ in Site), default=1
    )
    title = models.CharField(max_length=200)
    url = models.CharField(max_length=150)
    wished_price = models.IntegerField(default=0)
    available_price = models.IntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        if self.title:
            return self.title
        else:
            return self.url.split('/')[-1].split('.')[0]

