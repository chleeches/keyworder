import scrapy
from datetime import datetime 
from ..items import FinancialItem


class FinancialSpider(scrapy.Spider):
    name = "financial"
    start_urls = [
        'https://www.fnnews.com/',
        # 'https://www.fnnews.com/section/002008000',
        # 'https://www.fnnews.com/section/001001000',
        # 'https://www.fnnews.com/section/001003000',
        # 'https://www.fnnews.com/section/002005000',
        # 'https://www.fnnews.com/section/001002000',
        # 'https://www.fnnews.com/section/005000000',
    ]

    def parse(self, response):
        for url in response.css('ul.list_art li a::attr(href)'):
            yield response.follow(url, callback=self.parseArticle)

    def parseArticle(self, response):
        item = FinancialItem()
        item['url'] = response.url
        item['title'] = response.css('div.view_hd h1.tit_view::text').get()
        item['content'] = response.css('div#article_content::text').getall()
        item['timestamp'] = response.css('div.view_hd div.byline em::text').getall()[1]

        item['timestamp'] = datetime.strptime(item['timestamp'], '입력 %Y.%m.%d %H:%M')
        yield item
        