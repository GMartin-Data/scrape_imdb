import scrapy


class FilmspiderSpider(scrapy.Spider):
    name = "filmspider"
    allowed_domains = ["imdb.com"]
    start_urls = ["https://imdb.com"]

    def parse(self, response):
        pass
