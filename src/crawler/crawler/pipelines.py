import re


class ArticlePipeline:
    def open_spider(self, spider):
        spider.logger.info('Article process pipeline opened (started)')

    def process_item(self, item, spider):
        item['title'] = item.get('title').strip()
        item['content'] = {re.sub('\s+', ' ', paragraph.strip()) for paragraph in item.get('content')}
        item['content'] = filter(lambda x: len(x) > 0, item['content'])
        item['content'] = '\n'.join(item['content'])
        return item

    def close_spider(self, spider):
        spider.logger.info('Article process pipeline closed (finished)')
