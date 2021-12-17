import json
from pprint import pprint
import logging
import scrapy
from lxml import html
from ..items import PinsiderItemPosts, PinsiderItemRelease


class PinSpider(scrapy.Spider):
    name = 'pin'
    allowed_domains = ['blog.python.org']
    start_urls = ['http://blog.python.org/']
    test_mode = False
    max_rec_deep = 1

    def parse(self, response, **kwargs):
        # ===TMP===
        # Counter recursion
        try:
            rec_counter = int(response.cb_kwargs['rec_counter'])
            if self.test_mode and rec_counter > self.max_rec_deep:
                logging.info('Stop recursion')
                return
            rec_counter += 1
        except:
            rec_counter = 0
        # =========

        logging.info(f'------Page {response.url}')

        tree = html.fromstring(response.text)

        # All blocks with posts
        post_blocks = tree.xpath('//div[@class="date-outer"]')

        for post_num, post_block in enumerate(post_blocks):
            # Post Item
            item = PinsiderItemPosts()
            item['post_id'] = get_post_id(post_block)

            # Check post id
            if not item['post_id']:
                logging.warning(f'POST ID. Post number: {post_num}. URL: {response.url}')
                continue

            item['date'] = get_post_date(post_block)
            item['title'] = get_post_title(post_block)
            item['content'] = get_post_content(post_block)
            item['author'] = get_post_author(post_block)

            # Check other post data
            post_check_and_logging(item)

            logging.info(f'------------Item POST  {item["post_id"]}')

            yield item

            # Release links
            release_links = get_releases_links(post_block)

            # Callback to parse releases
            for release_link in release_links:
                yield scrapy.Request(url=release_link,
                                     callback=self.parse_release,
                                     dont_filter=True,
                                     cb_kwargs={
                                             'post_id': item['post_id']
                                     })

            if self.test_mode:
                break

        # Pagination
        older_link = get_older_link(tree)
        if older_link:
            yield scrapy.Request(url=older_link,
                                 callback=self.parse,
                                 dont_filter=True,
                                 cb_kwargs={
                                         'rec_counter': rec_counter
                                 })


    def parse_release(self, response, **kwargs):
        tree = html.fromstring(response.text)

        # Release Item
        item = PinsiderItemRelease()
        item['post_id'] = response.cb_kwargs['post_id']
        item['release_id'] = response.url
        item['title'] = get_release_title(tree)
        item['h1'] = item['title']
        item['date'] = get_release_date(tree)
        item['content'] = get_release_content(tree)
        item['peplinks'] = get_release_peplinks(tree)
        item['filedata'] = get_release_file_data(tree)

        # Check release data
        release_check_and_logging(item)

        logging.info(f'------------Item RELEASE {item["release_id"]}')

        yield item


# Parse post methods
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

def get_post_content(post_block):
    all_text = []
    for t in post_block.xpath('.//*/text()'):
        t = t.strip()
        if t == '\n' or t == '':
            continue
        all_text.append(t)
    return ' | '.join(all_text)

def get_post_author(post_block):
    try:
        return post_block.xpath('.//span[@class="post-author vcard"]/span/text()')[0]
    except:
        return ''

def get_releases_links(post_block):
    all_links = post_block.xpath('.//a[contains(@href, "/downloads/release/")]/@href')
    return {t.strip() for t in all_links if t}

def get_older_link(tree):
    try:
        return tree.xpath('//a[contains(@id, "older-link")]/@href')[0]
    except:
        return ''

def post_check_and_logging(item):
    for k, v in item.items():
        if not v:
            logging.warning(f'No {k}. PostID: {item["post_id"]}')


# Parse release methods
def get_release_title(tree):
    try:
        return tree.xpath('//h1[@class="page-title"]/text()')[0].strip()
    except:
        return ''

def get_release_date(tree):
    try:
        return tree.xpath('//article[@class="text"]//*[contains(text(), "Date:")]/../text()')[0].strip()
    except:
        return ''

def get_release_content(tree):
    all_text = []
    for t in tree.xpath('//article[@class="text"]//*/text()'):
        t = t.strip()
        if t == '\n' or t == '':
            continue
        all_text.append(t)
    return ' | '.join(all_text)

def get_release_file_data(tree):
    results = []
    html_table_block = tree.xpath('//article[@class="text"]//table')
    if not html_table_block:
        return ''

    table_headers = html_table_block[0].xpath('./thead/tr/th/text()')

    for tr in html_table_block[0].xpath('./tbody/tr'):
        body_list_block = []
        for td in tr.xpath('./td'):
            t = td.xpath('./a/@href | ./text()')
            if not t:
                body_list_block.append('')
                continue
            body_list_block.append(t[0])
        d = dict(zip(table_headers, body_list_block))
        results.append(d)

    try:
        return json.dumps(results)
    except:
        return ''

def get_release_peplinks(tree):
    all_links = []

    for t in tree.xpath('//article[@class="text"]//*[contains(@href, "dev/peps/pep-")]'):
        try:
            all_links.append(
                    {
                            t.xpath('./text()')[0].strip() : t.xpath('./@href')[0].strip()
                    }
            )
        except:
            continue

    try:
        return json.dumps(all_links)
    except:
        return ''

def release_check_and_logging(item):
    for k, v in item.items():
        if not v:
            logging.warning(f'No {k}. ReleaseID: {item["release_id"]}')