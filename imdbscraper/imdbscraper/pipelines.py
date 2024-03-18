# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import sqlite3

from itemadapter import ItemAdapter


def convert_duration(duration: str) -> int:
    """Convert a duration string to its minutes counterpart"""
    if "h" not in duration:
        minutes = int(duration.replace("m", "").strip())
    elif "m" not in duration:
        minutes = int(duration.replace("h", "").strip())
    else:
        duration = (duration
                    .replace("m", "")
                    .split("h"))
        hours, minutes = (int(elem.strip())
                          for elem in duration)
        minutes = hours * 60 + minutes
    return minutes


class CleanFilmPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        field_names = adapter.field_names() 
        LIST_FIELDS = ("main_casting", "genres", "countries")

        # Strip trailing spaces for non list fields
        for field_name in field_names:
            if field_name not in LIST_FIELDS:
                value = adapter.get(field_name)
                try:
                    adapter[field_name] = value.strip()
                except AttributeError:
                    adapter[field_name] = None

        # Join elements for list fields
        for field_name in LIST_FIELDS:
            value = adapter.get(field_name)
            adapter[field_name] = ", ".join(value)

        # Remove "Titre original : "
        tor = adapter.get("original_title")
        if tor is not None:
            adapter["original_title"] = tor.replace("Original title: ", "")

        # Convert score to float
        score = adapter.get("score")
        try:
            score = float(score.strip().replace(",", "."))
        except AttributeError:
            score = None
        
        # Convert year to int
        year = adapter.get("year")
        try:
            adapter["year"] = int(year)
        except AttributeError:
            adapter["year"] = None

        # Convert duration to minutes
        duration = adapter.get("duration")
        try:
           adapter["duration"] = convert_duration(duration)
        except Exception as e:
            adapter["duration"] = None
        
        return item
        

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
