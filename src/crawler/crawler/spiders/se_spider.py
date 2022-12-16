import scrapy
from ..items import SeoulItem


class SeoulSpider(scrapy.Spider):
    name = "seoul"
    start_urls = [
        'https://www.sedaily.com/NewsView/26EWVR1X5H'
    ]

    def parse(self, response):
        item = SeoulItem()
        item['url'] = response.url
        item['title'] = response.css('div.article_head h1.art_tit::text').get()
        item['content'] = response.css('div.article_view::text').getall()
        item['timestamp'] = response.css('div.article_info span.url_txt::text').get()
        yield item
