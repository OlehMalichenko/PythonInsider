import logging
import sqlite3
from pprint import pprint

if __name__ == '__main__':
    conn = sqlite3.connect('pinsider.db')
    curr = conn.cursor()

    curr.execute("""SELECT post_id, date, title, author FROM posts_tb""")
    data_posts = curr.fetchall()

    curr.execute("""SELECT post_id, release_id, date, title FROM releases_tb""")
    data_releases = curr.fetchall()

    # pprint(data_posts)
    print(f'Posts count {len(data_posts)}')

    # pprint(data_releases)
    print(f'Releases count {len(data_releases)}')


