# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import sqlite3

from itemadapter import ItemAdapter


class StoreSQLitePipeline:
    def __init__(self):
        self.con = sqlite3.connect("imdb.db")
        self.cur = self.con.cursor()
        self.create_table()

    def create_table(self):
        self.cur.execute("""
                         CREATE TABLE IF NOT EXISTS films(
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            title TEXT,
                            original_title TEXT,
                            score REAL,
                            year INTEGER,
                            audience TEXT,
                            duration INTEGER,
                            genres TEXT,
                            synopsis TEXT,
                            main_casting TEXT,
                            countries TEXT
                         )
                         """)
        
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        self.cur.execute(
            """INSERT INTO films (
            title, original_title, score, year, audience, duration, genres, synopsis, main_casting, countries
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                adapter.get("title"),
                adapter.get("original_title"),
                adapter.get("score"),
                adapter.get("year"),
                adapter.get("audience"),
                adapter.get("duration"),
                adapter.get("genres"),
                adapter.get("synopsis"),
                adapter.get("main_casting"),
                adapter.get("countries")
            )
        )
        self.con.commit()
        return item

    def close_spider(self, spider):
        self.cur.close()
        self.con.close()
