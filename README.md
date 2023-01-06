# Keyworder
오늘의 관심사를 알려줄 'Keyworder'로 하루를 시작하세요!

## 사용법
1. 프로그램에 사용할 환경변수 설정파일(.env) 생성
```
POSTGRES_HOSTNAME={} # PostgreSQL DB hostname
POSTGRES_USER={} # PostgreSQL DB user name
POSTGRES_PASSWORD={} # PostgreSQL DB user password
POSTGRES_DB={} # PostgreSQL DB schema name
```
2. 프로그램 실행
``` shell
# docker-compose up -d
```
3. Crawling을 주기적으로 하기 위한 cron 설정
``` shell
# echo "30 * * * * $USER poetry run scrapy list | xargs -n 1 poetry run scrapy crawl" | cat >> /etc/cron.d/keyworder
```
