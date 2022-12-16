import scrapy
from ..items import HeraldItem


class HeraldSpider(scrapy.Spider):
    name = "herald"
    start_urls = [
        'http://news.heraldcorp.com/view.php?ud=20221215000731'
    ]

    def parse(self, response):
        item = HeraldItem()
        item['url'] = response.url
        item['title'] = response.css('li.article_title::text').get()
        item['content'] = response.css('div.article_view p::text').getall()
        item['timestamp'] = response.css('li.article_date::text').get()
        yield item
