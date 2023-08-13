from requests_html import HTMLSession

headers = {
    'authority': 'www.daraz.com.np',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
    'accept-language': 'en-US,en;q=0.5',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36',
}

params = {
    'q': 'mobiles',
}

s = HTMLSession()
s.headers.update(headers)
response = s.get('https://www.daraz.com.np/catalog/', params=params)
response.html.render(sleep=1, timeout=12)

titles = response.html.xpath('//*[@id="root"]/div/div[2]/div/div/div[1]/div[2]/div[1]/div/div/div[2]/div[2]/a')

for title in titles:
    print(title.text, list(title.absolute_links)[0],sep='\n')


