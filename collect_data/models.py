from bs4 import BeautifulSoup as bs
from playwright.sync_api import Playwright
from datetime import datetime

class Scrapper:
    def __init__(self, playwright:Playwright, keywords:str):
        self.keywords = keywords
        self.browser = playwright.chromium.launch()
        self.products = []

    @property
    def new_page(self):
        return self.browser.new_page()
    
    @property
    def new_id(self):
        return int(datetime.now().strftime("%Y%m%d%H%M%S%f"))

    def get_sastodeal_products(self):
        page = self.new_page
        page.goto(f"https://www.sastodeal.com/catalogsearch/result/?q={self.keywords}")
        soup = bs(page.content(), 'lxml')
        product_divs = soup.select('.product-item-info')
        for div in product_divs:
            self.products.append({
                'id': self.new_id,
                'from': 'Sastodeal',
                'title': div.select_one('.product-item-name a').text.strip(),
                'link':div.select_one('.product-item-name a').attrs.get('href'),
                'price':  div.select_one('.price').text,
                'image':div.select_one('img').attrs.get('src'),
            })

    def get_daraz_products(self):
        page = self.new_page
        page.goto('https://www.daraz.com.np/')  # go to url

        # find search box and enter our query:
        search_box = page.locator('input#q')
        search_box.type(self.keywords, delay=100)

        # then, we can either send Enter key:
        search_box.press("Enter")
        page.wait_for_timeout(5000)
        soup = bs(page.content(), 'lxml')
        product_divs  = soup.select('div[data-qa-locator="product-item"]')
        for div in product_divs:
            self.products.append({
                'id': self.new_id,
                'from': 'Daraz',
                'link': 'https:'+div.select_one('.title--wFj93 a').attrs.get('href').split('?')[0],
                'title': div.select_one('.title--wFj93 a').text.split('|')[0].strip(),
                'image': div.select_one('img').attrs.get('src'),
                'price': div.select_one('.price--NVB62 span').text,
            })

    def get_dealayo_products(self):
        page = self.new_page
        page.goto(f'https://www.dealayo.com/catalogsearch/result/?q={self.keywords}')

        soup = bs(page.content(), 'lxml')
        product_divs = soup.select('.item.product-item')    
        for div in product_divs:
            self.products.append({
                'id': self.new_id,
                'from': 'Dealayo',
                'link': div.select_one('.product-name a').attrs.get('href'),
                'title': div.select_one('.product-name a').text,
                'image': div.select_one('.amda-product-top a.product-image img').attrs.get('src'),
                'price': div.select_one('.price').text,
            })

    def scrape(self):
        self.get_daraz_products()
        self.get_sastodeal_products()
        self.get_dealayo_products()