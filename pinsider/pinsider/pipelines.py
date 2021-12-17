# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

import sqlite3


class PinsiderPipeline:

    def __init__(self):
        self.create_connection()
        self.create_tables()

    def create_connection(self):
        self.conn = sqlite3.connect('pinsider.db')
        self.curr = self.conn.cursor()

    def create_tables(self):
        query_posts = """
                        CREATE TABLE IF NOT EXISTS posts_tb
                        (
                            post_id TEXT,
                            date TEXT,
                            title TEXT,
                            content TEXT,
                            author TEXT,
                            PRIMARY KEY (post_id)
                        )
                      """
        query_releases = """
                            CREATE TABLE IF NOT EXISTS releases_tb
                            (
                                post_id TEXT,
                                release_id TEXT,
                                title TEXT,
                                h1 TEXT,
                                date TEXT,
                                content TEXT,
                                peplinks TEXT,
                                filedata TEXT,
                                PRIMARY KEY (release_id),
                                FOREIGN KEY (post_id) REFERENCES posts_tb (post_id) 
                                    ON DELETE CASCADE ON UPDATE NO ACTION
                            )
                          """
        for query in [query_posts, query_releases]:
            self.curr.execute(query)
            self.conn.commit()

    def process_item(self, item, spider):
        name_of_item_class = str(item.__class__.__name__)
        # print(f'Name of class {name_of_item_class}')
        if 'PinsiderItemPosts' in name_of_item_class:
            self.store_db_post(item)
        elif 'PinsiderItemRelease' in name_of_item_class:
            self.store_db_release(item)

        return item

    def store_db_post(self, item):
        self.curr.execute(
            """INSERT OR IGNORE INTO posts_tb VALUES (?,?,?,?,?)""",
            (
                    item['post_id'],
                    item['date'],
                    item['title'],
                    item['content'],
                    item['author']
            )
        )
        self.conn.commit()

    def store_db_release(self, item):
        self.curr.execute(
                """INSERT OR IGNORE INTO releases_tb VALUES (?,?,?,?,?,?,?,?)""",
                (
                        item['post_id'],
                        item['release_id'],
                        item['title'],
                        item['h1'],
                        item['date'],
                        item['content'],
                        item['peplinks'],
                        item['filedata']
                )
        )
        self.conn.commit()
