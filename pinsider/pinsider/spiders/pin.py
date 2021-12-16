from pprint import pprint

import scrapy
from lxml import html
from ..items import PinsiderItemPosts, PinsiderItemRelease


class PinSpider(scrapy.Spider):
    name = 'pin'
    allowed_domains = ['blog.python.org']
    start_urls = ['http://blog.python.org/']

    def parse(self, response, **kwargs):
        response_url = response.url
        tree = html.fromstring(response.text)
        post_blocks = tree.xpath('//div[@class="date-outer"]')

        for post_block in post_blocks:
            item = PinsiderItemPosts()
            item['date'] = get_post_date(post_block)
            item['post_id'] = get_post_id(post_block)
            item['title'] = get_post_title(post_block)
            item['content'] = get_content(post_block)
            item['author'] = get_author(post_block)
            # yield item

            break

    def parse_release(self, response, **kwargs):
        pass

def get_post_date(post_block):
    try:
        return post_block.xpath('.//h2[@class="date-header"]//span/text()')[0]
    except:
        return ''

def get_post_id(post_block):
    try:
        return post_block.xpath('.//h3[contains(@class, "post-title")]/a/@href')[0]
    except:
        return ''

def get_post_title(post_block):
    try:
        return post_block.xpath('.//h3[contains(@class, "post-title")]/a/text()')[0]
    except:
        return ''

def get_content(post_block):
    all_text = []
    for t in post_block.xpath('.//*/text()'):
        t = t.strip()
        if t == '\n' or t == '':
            continue
        all_text.append(t)
    return ' | '.join(all_text)

def get_author(post_block):
    try:
        return post_block.xpath('.//span[@class="post-author vcard"]/span/text()')[0]
    except:
        return ''