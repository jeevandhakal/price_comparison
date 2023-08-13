from django.shortcuts import render
from django.views.decorators.cache import cache_page

from collect_data.models import Scrapper
from time import perf_counter
from asyncio import run


def index(request):
    return render(request, 'index.html')


@cache_page(60 * 15)
def search(request):
    search_input = request.GET['search']
    start = perf_counter()
    scrapper = Scrapper(search_input)
    run(scrapper.scrape())
    print("scrape completed in - ", perf_counter() - start)
    start = perf_counter()
    scrapper.sort()
    print("sort completed in - ", perf_counter() - start)
    request.session['products'] = scrapper.products
    return render(request, 'index.html', {'products':scrapper.products,})

# 33.32489131600596