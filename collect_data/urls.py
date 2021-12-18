from django.urls import path
from .views import Index,wished_product_form

urlpatterns = [
    path('', Index.as_view(), name='index'),
    # path('wished_product/', wished_product, name="wished_product"),
    path('wished_product_form/',wished_product_form,name="wished_product_form"),
]
