from django.db import models
from user.models import CustomUser



class WishList(models.Model):
    title= models.CharField(max_length=150)
    url= models.CharField(max_length=150)
    wanted_price= models.DecimalField(decimal_places=1,max_digits=5,default=0)
    available_price= models.DecimalField(decimal_places=1,max_digits=5,default=0)
    user= models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.title

    
    

 