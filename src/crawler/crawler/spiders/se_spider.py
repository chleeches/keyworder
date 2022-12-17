import scrapy
from datetime import datetime
from ..items import SeoulItem


class SeoulSpider(scrapy.Spider):
    name = "seoul"
    start_urls = [
        'https://www.sedaily.com/v/NewsMain/GA',
        'https://www.sedaily.com/v/NewsMain/GB',
        'https://www.sedaily.com/v/NewsMain/GC',
        'https://www.sedaily.com/v/NewsMain/GD',
        'https://www.sedaily.com/v/NewsMain/GE',
        'https://www.sedaily.com/v/NewsMain/GK',
        'https://www.sedaily.com/v/NewsMain/GF',
        'https://www.sedaily.com/v/NewsMain/GG',
        'https://www.sedaily.com/v/NewsMain/GH',
    ]

    def parse(self, response):
        for url in response.css('ul.sub_news_list div.article_tit a::attr(href)'):
            yield response.follow(url, callback=self.parseArticle)

    def parseArticle(self, response):
        item = SeoulItem()
        item['url'] = response.url
        item['title'] = response.css('div.article_head h1.art_tit::text').get()
        item['content'] = response.css('div.article_view::text').getall()
        item['timestamp'] = response.css('div.article_info span.url_txt::text').get()

        item['timestamp'] = datetime.strptime(item['timestamp'], '%Y-%m-%d %H:%M:%S')
        yield item
