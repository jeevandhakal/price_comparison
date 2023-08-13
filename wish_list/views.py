from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from wish_list.models import WishList
from wish_list.forms import WishListForm
from django.shortcuts import redirect


@login_required
def wished_product_form(request):

    if request.method=="POST":
        user= request.user
        product = {}
        wanted_price = request.POST.get("wished_price")

        available_price = int(''.join([i for i in product['price'] if i.isdigit()]))
        if available_price <= wanted_price:
            messages.warning(request, "Available price is already less, why do you want ?")
        else:
            WishList.objects.create(
                title=product['title'],
                url=product['link'],
                available_price=available_price, 
                wanted_price=wanted_price, user=user, 
                site=product['from']
            )
            messages.success(request,"If your wished_price is less than available_price , alert message in your email will be sent.")
            return redirect('index')

    form = WishListForm()
    return render(request,'wished_product_form.html', {'form': form})
