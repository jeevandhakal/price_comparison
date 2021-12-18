from bs4 import BeautifulSoup
import requests
from django.views.generic import View
from django.shortcuts import render
from .models import WishList
from user.models import CustomUser
from django.contrib.auth.decorators import login_required
from django.contrib import messages

class Index(View):

    template = "index.html"
    def get(self, request):
        return render(request, self.template)

    def post(self, request):
        search_input = request.POST['search']

        

        urls = [
        {
            'name':'sastodeal',
            'link': "https://www.sastodeal.com/catalogsearch/result/?q=",
            },
        {
            'name': 'dealayo',
            'link': "https://www.dealayo.com/catalogsearch/result/?q=",
            },
        {
            'name': 'okdam',
            'link': "https://www.okdam.com/search?k=",
        },
        {
            'name': 'meroshopping',
            'link': "https://www.meroshopping.com/search/",
        },
        ]
        products = []
        for url in urls:
            search_url = url['link'] + search_input
            # check_internet_connection(request, search_url)
            req = requests.get(search_url)
            

            soup = BeautifulSoup(req.content, 'html5lib')

            if url['name'] == 'sastodeal':
                product_divs = soup.select('.item.product.product-item')

                for div in product_divs:
                    product = {}
                    product['from'] = url['name']
                    product['title'] = div.select_one('.product-item-name a').text
                    product['link'] = div.select_one('.product-item-name a')['href']
                    product['price'] =  div.select_one('.price').text
                    product['image'] = div.select_one('.product-image-photo')['src']
                    products.append(product)
          

            elif url['name'] == 'dealayo':
                product_divs = soup.select('.item.product-item')
                
                for div in product_divs:
                    product = {}
                    product['from'] = url['name']
                    product['title'] = div.select_one('.product-name a').text
                    product['link'] = div.select_one('.product-name a')['href']
                    product['price'] =  div.select_one('.price').text
                    product['image'] = div.select_one('.amda-product-top a.product-image img')['src']
                    products.append(product)

            elif url['name'] == 'okdam':
                product_divs = soup.select('.pro-wrap a')

                for div in product_divs:
                    product = {}
                    product['from'] = url['name']
                    product['title'] = div['title']
                    product['link'] = div['href']
                    product['price'] =  div.select_one('.og-price').text
                    product['image'] = div.select_one('.product-box img')['data-src']
                    products.append(product)
            
            
            elif url['name'] == 'meroshopping':
                search_input = '-'.join(search_input)
                search_url = url['link'] + search_input
                page = requests.get(search_url)

                soup = BeautifulSoup(page.content, 'html5lib')
                product_divs = soup.select('.product')

                for div in product_divs:
                    product = {}
                    product['from'] = url['name']
                    product['title'] = div.select_one('.prname span').text
                    product['link'] = "https://www.meroshopping.com/" + div.select_one('.product a')['href']
                    product['price'] =  div.select_one('.all-price').text
                    product['image'] = "https://www.meroshopping.com/" + div.select_one('img')['src']
                    products.append(product)

        return render(request, self.template, {'products':products})


# @login_required
# def wished_product(request):
#     if request.method=="POST":
#         user = request.user
#         title = request.POST.get("title")
#         link = request.POST.get("link")
#         price = request.POST.get("price")
#         if price:
#             price = int(''.join([i for i in price if i.isdigit()]))
#         wanted_price = request.POST.get("wished_price")
#         if price <= wanted_price:
#             messages.warning(request, "Available price is already lesseer, why do you want ?")
#         else:
#             data= WishList(title=title,url=link,available_price=price,wanted_price=wanted_price,user=user)
#             data.save()
#             messages.success(request,"If your wished_price is less than available_price , alert message in the email will shown.")
#     return render(request, 'index.html')

@login_required
def wished_product_form(request):
    if request.method=="POST":
        user= request.user
        title= request.POST.get("title")
        link= request.POST.get("link")
        available_price= request.POST.get("price")
        if available_price:
            available_price = int(''.join([i for i in price if i.isdigit()]))
        wanted_price = request.POST.get("wished_price")
        if available_price <= wanted_price:
            messages.warning(request, "Available price is already lesseer, why do you want ?")
        else:
            data= WishList(title=title,url=link,available_price=available_price,wanted_price=wanted_price,user=user)
            data.save()
            messages.success(request,"If your wished_price is less than available_price , alert message in the email will shown.")
    return render(request,'wished_product_form.html')

    
        
    