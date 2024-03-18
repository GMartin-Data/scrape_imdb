# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ImdbscraperItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class FilmItem(scrapy.Item):
    title = scrapy.Field()
    original_title = scrapy.Field()
    score = scrapy.Field()
    year = scrapy.Field()
    audience = scrapy.Field()
    duration = scrapy.Field()
    genres = scrapy.Field()
    synopsis = scrapy.Field()
    main_casting = scrapy.Field()
    countries = scrapy.Field()
