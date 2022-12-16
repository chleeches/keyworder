import scrapy
from ..items import FinancialItem


class FinancialSpider(scrapy.Spider):
    name = "financial"
    start_urls = [
        'https://www.fnnews.com/news/202212151520156745'
    ]

    def parse(self, response):
        item = FinancialItem()
        item['url'] = response.url
        item['title'] = response.css('div.view_hd h1.tit_view::text').get()
        item['content'] = response.css('div#article_content::text').getall()
        item['timestamp'] = response.css('div.view_hd div.byline em').get(1)
        yield item
        