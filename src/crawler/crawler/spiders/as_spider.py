import scrapy
from ..items import AsiaItem


class AsiaSpider(scrapy.Spider):
    name = "asia"
    start_urls = [
        'https://www.asiae.co.kr/article/economic-general/2022121516393245785'
    ]

    def parse(self, response):
        item = AsiaItem()
        item['url'] = response.url
        item['title'] = response.css('div.area_title h3::text').get()
        item['content'] = response.css('div#txt_area p::text').getall()
        item['timestamp'] = response.css('div.area_util p.user_data::text').getall()[2]
        yield item
