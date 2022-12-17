import scrapy
from datetime import datetime
from ..items import HankyungItem


class HankyungSpider(scrapy.Spider):
    name = "hankyung"
    start_urls = [
        'https://www.hankyung.com/economy',
        'https://www.hankyung.com/financial-market',
        'https://www.hankyung.com/industry',
        'https://www.hankyung.com/politics',
        'https://www.hankyung.com/society',
        'https://www.hankyung.com/international',
        'https://www.hankyung.com/it',
        'https://www.hankyung.com/life',
        'https://www.hankyung.com/culture',
        'https://www.hankyung.com/golf',
        'https://www.hankyung.com/sports',
        'https://www.hankyung.com/entertainment'
    ]

    def parse(self, response):
        for url in response.css('ul.news-list h3.news-tit a::attr(href)'):
            yield response.follow(url, callback=self.parseArticle)

    def parseArticle(self, response):
        item = HankyungItem()
        item['url'] = response.url
        item['title'] = response.css('article.article-contents h1.headline::text').get()
        item['content'] = response.css('div#articletxt::text').getall()
        item['timestamp'] = response.css('div.article-timestamp span.txt-date::text').get()

        item['timestamp'] = datetime.strptime(item['timestamp'], '%Y.%m.%d %H:%M')
        yield item
        