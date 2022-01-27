from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import WishList
import requests

from bs4 import BeautifulSoup
import html5lib
from django.core.mail import send_mail
from django.conf import settings

import time

def notify_user(product, price):
    mess= f"Hello {product.user.first_name}! \n The product({product.title}), you wished is now available for price {price} \nPlease visit {product.url} to purchase it.\nThanks!!"
    send_mail(
        "Product available",
        mess,
        settings.EMAIL_HOST_USER,
        [product.user.email],
        fail_silently= False
    )

def only_digit(price):
    return int(''.join([i for i in price if i.isdigit()]))

@receiver(post_save, sender=WishList)
def track_price(sender, instance, created, **kwargs):
    if created:
        while True:
            req = requests(instance.url)
            soup = BeautifulSoup(req.content, 'html5lib')

            if instance.site == 'sastodeal' or 'dealayo':
                available_price =  soup.select_one('.price').text
            
            elif instance.site == 'okdam':
                available_price =  soup.select_one('.og-price').text

            elif instance.site == 'meroshopping':
                available_price =  soup.select_one('.all-price').text

            available_price = only_digit(available_price)
            if available_price <= instance.wanted_price:
                notify_user(instance, available_price)
                break
            
            time.sleep(86400)
           
            