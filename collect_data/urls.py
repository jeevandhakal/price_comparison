from django.urls import path
from .views import *

urlpatterns = [
    path('', index , name='index'),
    path('search/', search, name='search'),
    # path('wished_product/', wished_product, name="wished_product"),
    path('wished_product_form/',wished_product_form,name="wished_product_form"),
    path('wished_product_form/<int:id>/',wished_product_form,name="wished_product_form"),
]
