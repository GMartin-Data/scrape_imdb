from typing import Iterable

import scrapy

from imdbscraper.items import FilmItem

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
            film_relative_url = film.css("a::attr(href)").get()
            film_url = f"https://imdb.com{film_relative_url}"
            yield response.follow(film_url,
                                  callback = self.parse_film_page,
                                  headers=HEADERS)
            
    def parse_film_page(self, response):
        # Intermediary tag for year, audience, and duration
        TOP_INFO = "h1[data-testid='hero__pageTitle'] ~ ul"

        # Genres
        genres = response.css("div[data-testid='genres'] a")
        genres = [genre.css("a span::text").get() for genre in genres]

        # Main Casting
        credits =  response.css("li[data-testid='title-pc-principal-credit']")[2]
        actors = credits.css("div > ul li")
        casting = [actor.css("a::text").get()
                   for actor in actors]
        
        film_item = FilmItem()

        film_item["title"] = response.css("span[data-testid='hero__primary-text']::text").get()
        film_item["original_title"] = response.css("h1 + div::text").get()
        film_item["score"] = response.css("div[data-testid='hero-rating-bar__aggregate-rating__score'] > span ::text").get()
        film_item["year"] = response.css(f"{TOP_INFO} li:nth-child(1) > a ::text").get()
        film_item["audience"] = response.css(f"{TOP_INFO} li:nth-child(2) > a ::text").get()
        film_item["duration"] = response.css(f"{TOP_INFO} li:nth-child(3) ::text").get()
        film_item["genres"] = genres
        film_item["synopsis"] = response.css("span[data-testid='plot-xs_to_m'] ::text").get()
        film_item["main_casting"] = casting
        film_item["countries"] = response.css("li[data-testid='title-details-origin'] a::text").get()

        yield film_item
