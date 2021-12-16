import sqlite3

if __name__ == '__main__':

    conn = sqlite3.connect('pinsider.db')
    curr = conn.cursor()



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
        curr.execute(query)
        conn.commit()
