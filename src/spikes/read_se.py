# 서울경제 기사 본문 가져오기

from collections import Counter
from modules.get_texts import get_html
from bs4 import BeautifulSoup
from konlpy.tag import Okt


def extract_mk_text(html):
    soup = BeautifulSoup(html, 'html.parser')
    article = soup.select_one('div.con_left')
    
    return article

if __name__ == '__main__':
    url = 'https://www.sedaily.com/NewsView/26DGIOC178?OutLink=nstand'
    html = get_html(url)
    article = extract_mk_text(html)

    okt = Okt()
    nouns = okt.nouns(article.text)
    print(Counter(nouns).most_common(5))
    


