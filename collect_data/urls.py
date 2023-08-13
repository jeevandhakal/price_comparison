from django.urls import path
from collect_data.views import index, search

urlpatterns = [
    path('', index , name='index'),
    path('search/', search, name='search'),
]
