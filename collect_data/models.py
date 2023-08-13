from bs4 import BeautifulSoup as bs
from playwright.async_api import async_playwright
from datetime import datetime
from asyncio import gather


class Scrapper:
    def __init__(self, keywords:str):
        self.keywords = keywords
        self.products = []
    
    @property
    def new_id(self):
        return int(datetime.now().strftime("%Y%m%d%H%M%S%f"))

    async def scrape_sastodeal(self):
        async with async_playwright() as p:
            browser = await p.chromium.launch()
            page = await browser.new_page()
            await page.goto(f"https://www.sastodeal.com/catalogsearch/result/?q={self.keywords}")
            content = await page.content()
            soup = bs(content, 'lxml')
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

    async def scrape_daraz(self):
        async with async_playwright() as p:
            browser = await p.chromium.launch()
            page = await browser.new_page()
            await page.goto('https://www.daraz.com.np/')  # go to url

            # find search box and enter our query:
            search_box = page.locator('input#q')
            await search_box.type(self.keywords, delay=100)

            # then, we can either send Enter key:
            await search_box.press("Enter")
            await page.wait_for_timeout(1000)
            content = await page.content()
            soup = bs(content, 'lxml')
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

    async def scrape_dealayo(self):
        async with async_playwright() as p:
            browser = await p.chromium.launch()
            page = await browser.new_page()
            await page.goto(f'https://www.dealayo.com/catalogsearch/result/?q={self.keywords}')
            content = await page.content()
            soup = bs(content, 'lxml')
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

    async def scrape(self):
        tasks = [
        self.scrape_daraz(),
        self.scrape_sastodeal(),
        self.scrape_dealayo()
        ]
        await gather(*tasks)

    def sort(self, reverse: bool = False):
        def get_price_value(product_dict):
            price = product_dict['price']
            return int(''.join([i for i in price if i.isdigit()]))

        self.products = sorted(self.products, key=get_price_value, reverse=reverse)
        
