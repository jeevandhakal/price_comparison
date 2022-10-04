from django.core.mail import send_mail
from price_comparision import settings
from collect_data.models import WishList

from bs4 import BeautifulSoup
import html5lib
import requests

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


def track_wishlist():
    wish_list = WishList.objects.all()
    for wish in wish_list:
        req = requests(wish.url)
        soup = BeautifulSoup(req.content, 'html5lib')
        available_price =  soup.select_one('p').text
        print(available_price)


        if wish.site == 'sastodeal' or 'dealayo':
            available_price =  soup.select_one('.price').text

        elif wish.site == 'okdam':
            available_price =  soup.select_one('.og-price').text

        elif wish.site == 'meroshopping':
            available_price =  soup.select_one('.all-price').text

        available_price = only_digit(available_price)
        if available_price <= wish.wanted_price:
            notify_user(wish, available_price)

