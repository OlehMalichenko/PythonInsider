import scrapy


class PinSpider(scrapy.Spider):
    name = 'pin'
    allowed_domains = ['blog.python.org']
    start_urls = ['http://blog.python.org/']

    def parse(self, response):
        pass
