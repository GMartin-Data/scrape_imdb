import scrapy


class FilmspiderSpider(scrapy.Spider):
    name = "filmspider"
    allowed_domains = ["imdb.com"]
    start_urls = ["https://www.imdb.com/chart/top/?ref_=nv_mv_250"]

    def parse(self, response):
        pass
