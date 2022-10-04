from django.db import models
from user.models import CustomUser

from django.dispatch import receiver
from django.db.models.signals import post_save

from bs4 import BeautifulSoup
import html5lib
import requests

import time

class WishList(models.Model):
    title = models.CharField(max_length=150)
    url = models.CharField(max_length=150)
    wanted_price = models.IntegerField(default=0)
    available_price = models.IntegerField(default=0)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    site = models.CharField(max_length=50)
    
    def __str__(self):
        return self.title

    
@receiver(post_save, sender=WishList)
def wishlist_post_save_handler(sender, instance, created, *args, **kwargs):
    if created:
        pass
    else:
        print(instance.url)
        
        while True:
            with open('/home/jeevan/Task/main.html', 'r') as file:
                content = file.read()
                soup = BeautifulSoup(content, 'html5lib')
                available_price =  int(soup.select_one('p').text)

                if available_price <= instance.wanted_price:
                    print('the product is available for', available_price)
                    break
                
                time.sleep(60)

        

    