from collections import defaultdict, Counter
from modules.get_texts import get_html, extract_text
from konlpy.tag import Okt


if __name__ == '__main__':
    url = 'http://news.mk.co.kr/sforward.php?domain=news&sc=30000001&year=2022&no=967741'
    html = get_html(url)

    okt = Okt()
    counter = defaultdict(int)
    for text in extract_text(html):
        nouns = okt.nouns(text)
        for noun in nouns:
            counter[noun] += 1
    print(Counter(counter))
