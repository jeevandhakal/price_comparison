from django.urls import path
from .views import *

urlpatterns = [
    path('', index , name='index'),
    path('search/', search, name='search'),
    # path('wished_product/', wished_product, name="wished_product"),
]
