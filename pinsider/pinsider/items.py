# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class PinsiderItemPosts(scrapy.Item):
    post_id = scrapy.Field()
    date = scrapy.Field()
    title = scrapy.Field()
    content = scrapy.Field()
    author = scrapy.Field()


class PinsiderItemRelease(scrapy.Item):
    post_id = scrapy.Field()
    release_id = scrapy.Field()
    title = scrapy.Field()
    h1 = scrapy.Field()
    date = scrapy.Field()
    content = scrapy.Field()
    peplinks = scrapy.Field()
    filedata = scrapy.Field()

