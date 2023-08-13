from django.shortcuts import render
from playwright.sync_api import sync_playwright
from django.views.decorators.cache import cache_page

from collect_data.models import Scrapper
from time import perf_counter


def index(request):
    return render(request, 'index.html')


@cache_page(60 * 15)
def search(request):
    search_input = request.GET['search']
    start = perf_counter()
    with sync_playwright() as pw:
        scrapper = Scrapper(pw, search_input)
        scrapper.scrape()
    print("request completed in - ", perf_counter() - start)
    request.session['products'] = scrapper.products
    return render(request, 'index.html', {'products':scrapper.products,})

# 33.32489131600596