from typing import Iterable
import scrapy


HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Accept-Language": "fr"
}

class FilmspiderSpider(scrapy.Spider):
    name = "filmspider"
    allowed_domains = ["imdb.com"]
    start_urls = ["https://www.imdb.com/chart/top/?ref_=nv_mv_250"]

    def start_requests(self):
        yield scrapy.Request(
            url=self.start_urls[0],
            headers = HEADERS,
        )
    
    def parse(self, response):
        films = response.css("div[data-testid='chart-layout-main-column'] > ul li")
        for film in films:
            yield {
                "url_end": film.css("a::attr(href)").get()
            }
