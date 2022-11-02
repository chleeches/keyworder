from collections import defaultdict
from bs4 import BeautifulSoup
from bs4.element import Comment
import requests
import re
from collections import Counter


EXTRACT = ['[document]', 'noscript', 'script', 'header', 'head', 'html', 'meta', 'input', 'style']

def tag_visible(element):
    if element.parent.name in EXTRACT \
        or isinstance(element, Comment) \
        or re.match(r'[\s\r\n]+', str(element)):
        return False
    return True

def extract_text(html):
    soup = BeautifulSoup(html, 'html.parser')
    texts = soup.extract('a').findAll(text=True)
    visible_texts = filter(tag_visible, texts)  
    return visible_texts

def get_html(url):
    response = requests.get(url)
    return response.text


if __name__ == '__main__':
    url = 'https://www.hankyung.com/economy/article/2022103168131?utm_source=naver&utm_medium=naver_newsstandcast&utm_campaign=newsstandcast_naver_all'
    html = get_html(url)
    texts = extract_text(html)
    counter = Counter(texts)
    print(counter)