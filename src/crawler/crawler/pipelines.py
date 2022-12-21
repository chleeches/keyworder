import os
import re
import psycopg2
from konlpy.tag import Okt
from collections import Counter


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

class KeywordPipeline:
    def open_spider(self, spider):
        spider.logger.info('Keyword extraction pipeline opened (started)')
        self.okt = Okt()
    
    def process_item(self, item, spider):
        for src, dest in zip(('title', 'content'), ('title_keywords', 'content_keywords')):
            nouns = self.okt.nouns(item[src])
            counter = Counter(nouns)
            item[dest] = dict(counter)
        return item

    def close_spider(self, spider):
        spider.logger.info('Keyword extraction pipeline closed (finished)')

class DatabasePipeline:
    def open_spider(self, spider):
        spider.logger.info('Database transaction pipeline opened (started)')
        hostname = os.environ("POSTGRES_HOSTNAME")
        username = os.environ("POSTGRES_USER")
        password = os.environ("POSTGRES_PASSWORD")
        database = os.environ("POSTGRES_DB")
        self.connection = psycopg2.connect(host=hostname, user=username, password=password, dbname=database)
        self.cursor = self.connection.cursor()
    
    def process_item(self, item, spider):
        self.cursor.execute("""
            INSERT INTO
            articles (url, title, content, created_at)
            VALUES (%s, %s, %s, %s)
        """, (
            item['url'],
            item['title'],
            item['content'],
            item['timestamp'],
        ))
        for keyword, cnt in item['keywords']:
            self.cursor.execute("""
                INSERT INTO
                keywords (url, keyword, cnt)
                VALUES (%s, %s, %s)
            """, (
                item['url'],
                keyword,
                cnt,
            ))
        return item

    def close_spider(self, spider):
        self.cursor.close()
        self.connection.close()
        spider.logger.info('Database transaction pipeline closed (finished)')
