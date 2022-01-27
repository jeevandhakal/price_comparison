from django.db import models
from user.models import CustomUser

class WishList(models.Model):
    title = models.CharField(max_length=150)
    url = models.CharField(max_length=150)
    wanted_price = models.IntegerField(default=0)
    available_price = models.IntegerField(default=0)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    site = models.CharField(max_length=50)
    
    def __str__(self):
        return self.title

    
    

 