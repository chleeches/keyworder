import scrapy
from ..items import HankyungItem


class HankyungSpider(scrapy.Spider):
    name = "hankyung"
    start_urls = [
        'https://www.hankyung.com/economy/article/202212158845g?utm_source=naver&utm_medium=naver_newsstandcast&utm_campaign=newsstandcast_naver_all',
        'https://www.hankyung.com/economy/article/202212158930Y'
    ]

    def parse(self, response):
        item = HankyungItem()
        item['url'] = response.url
        item['title'] = response.css('article.article-contents h1.headline::text').get()
        item['content'] = response.css('div#articletxt::text').getall()
        item['timestamp'] = response.css('div.article-timestamp span.txt-date::text').get()
        yield item
        