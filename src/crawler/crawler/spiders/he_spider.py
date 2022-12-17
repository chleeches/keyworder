import scrapy
from datetime import datetime
from ..items import HeraldItem


class HeraldSpider(scrapy.Spider):
    name = "herald"
    start_urls = [
        'http://biz.heraldcorp.com/list.php?ct=010108000000',
        'http://biz.heraldcorp.com/list.php?ct=010104000000',
        'http://biz.heraldcorp.com/list.php?ct=010109000000',
        'http://biz.heraldcorp.com/list.php?ct=010110000000',
        'http://biz.heraldcorp.com/list.php?ct=010107000000',
        'http://biz.heraldcorp.com/list.php?ct=010504000000',
        'http://biz.heraldcorp.com/list.php?ct=010400000000',
    ]

    def parse(self, response):
        for url in response.css('div.list ul li a::attr(href)'):
            yield response.follow(url, callback=self.parseArticle)

    def parseArticle(self, response):
        item = HeraldItem()
        item['url'] = response.url
        item['title'] = response.css('li.article_title::text').get()
        item['content'] = response.css('div.article_view p::text').getall()
        item['timestamp'] = response.css('li.article_date::text').get()

        item['timestamp'] = datetime.strptime(item['timestamp'].strip(), '%Y.%m.%d %H:%M')
        yield item
