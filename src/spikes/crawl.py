from collections import Counter, defaultdict
import logging
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from konlpy.tag import Okt
import re
from modules.get_texts import get_html
from collections import deque


# 목표: 특정 URL 형식만 crawling 하도록 하기
'''
모든 링크 크롤링 하면서 regexp 해당하는 사이트 발견시 키워드 추출
'''

CONFIG = deque([
    {'url': 'https://www.mk.co.kr/', 'regexp': 'https:\/\/www\.mk\.co\.kr\/news\/.+\/\d', 'selector': 'div.news_cnt_detail_wrap'},
    {'url': 'https://www.sedaily.com/', 'regexp': 'https:\/\/www\.sedaily\.com\/NewsView\/.+', 'selector': 'div.con_left'}
])

logging.basicConfig(
    format='%(asctime)s %(levelname)s:%(message)s',
    level=logging.INFO)

class Crawler:
    def __init__(self, initial_nexts = []):
        self.okt = Okt()
        # self.visited_urls = []
        # self.urls_to_visit = targets
        self.visited = []
        self.nexts = initial_nexts

    def download_url(self, url):
        return requests.get(url).text

    def get_linked_urls(self, url, html):
        soup = BeautifulSoup(html, 'html.parser')
        for link in soup.find_all('a'):
            path = link.get('href')
            if path and path.startswith('/'):
                path = urljoin(url, path)
            yield path

    def add_next(self, url, regexp, selector):
        if url not in self.visited and url not in self.nexts:
            self.nexts.append({
                'url': url,
                'regexp': regexp,
                'selector': selector
            })

    def crawl(self, url, regexp, selector):
        html = self.download_url(url)
        for url in self.get_linked_urls(url, html):
            self.add_next(url, regexp, selector)

    def run(self):
        lst = []
        while self.nexts:
            target = self.nexts.popleft()
            logging.info('Crawling: {}'.format(target['url']))
            
            try:
                if re.match(target['regexp'], target['url']):
                    soup = BeautifulSoup(get_html(target['url']), 'html.parser')
                    article = soup.select_one(target['selector'])

                    nouns = self.okt.nouns(article.text)
                    print(Counter(nouns).most_common(5))
                    
                self.crawl(target['url'], target['regexp'], target['selector'])
            except Exception:
                logging.exception('Failed to crawl: {}'.format(target['url']))
            finally:
                self.visited.append(target['url'])
        return lst

if __name__ == '__main__':
    lst = Crawler(CONFIG).run()
    print(lst)
    