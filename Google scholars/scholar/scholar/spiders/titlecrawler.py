import scrapy
from urllib.parse import urlencode
from scrapy.exceptions import CloseSpider
from ..items import ScholarItem
API_KEY = '5f470cf6f9c5c1b154214ce6fac90111'
count = 0
def get_url(url):
    payload = {'api_key': API_KEY, 'url': url, 'country_code': 'us'}
    proxy_url = 'http://api.scraperapi.com/?' + urlencode(payload)
    return proxy_url
class TitlecrawlerSpider(scrapy.Spider):
    name = 'titlecrawler'
    #allowed_domains = ['api.scraperapi.com']

    def __init__(self, query=""):
        self.queries = query
        self.limit = 30

    def start_requests(self):
        # self.queries = ['Bahria University']
        # for query in queries:
        url = 'https://scholar.google.com/scholar?' + urlencode({'hl': 'en', 'q': self.queries})
        yield scrapy.Request(get_url(url), callback=self.parse, meta={'position': 0})

    def parse(self, response):
        item = ScholarItem()
        print(response.url)
        position = response.meta['position']
        for res in response.xpath('//*[@data-rp]'):
            global count
            temp = res.xpath('.//h3/a//text()').extract()
            if not temp:
                title = "[C] " + "".join(res.xpath('.//h3/span[@id]//text()').extract())
            else:
                title = "".join(temp)
            title=title.replace('""','').replace('.','')
            position += 1
            item['title'] = str(title)
            count += 1
            yield item
            if count == self.limit:
                raise CloseSpider('Limit Reached!')

        next_page = response.xpath('//td[@align="left"]/a/@href').extract_first()
        if next_page:
            url = "https://scholar.google.com" + next_page
            yield scrapy.Request(get_url(url), callback=self.parse, meta={'position': position})

