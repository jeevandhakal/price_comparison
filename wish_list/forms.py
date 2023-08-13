from django import forms
from django import forms
from wish_list.models import WishList


class WishListForm(forms.ModelForm):
    class Meta:
        model = WishList
        fields = ['site', 'url', 'wished_price']