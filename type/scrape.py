import requests
from bs4 import BeautifulSoup
import time
import csv
import datetime


csvlist = []
url_index = 'https://type.jp/job-1'
id = 1

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:58.0) Gecko/20100101 Firefox/58.0'}
headers['referer'] = 'https://www.google.co.jp'


for page in range(1,15):
    url = f'https://type.jp/job-1/area6-osaka_city/p{page}/'
    res = requests.get(url,headers)
    time.sleep(5)

    soup = BeautifulSoup(res.content, 'html.parser')
    job_cards = soup.find_all('p', class_='company')
    job_salarys = soup.find_all(class_='mod-table')
    job_card_heads = soup.find_all(class_='title')
    job_urls = soup.find_all(class_='title')

    for (job_card, job_salary, job_card_head, job_url) in zip(job_cards, job_salarys, job_card_heads, job_urls):
        td = job_salary.select('td')
        print([id, job_card.span.text, td[1].text.replace("\n"," ").replace("\r"," "), job_card_head.a.text, url_index + job_url.a.get('href')])
        csvlist.append([id, job_card.span.text,  td[1].text.replace("\n"," ").replace("\r"," "), job_card_head.a.text, url_index + job_url.a.get('href')])
        id += 1
    print(str(page) + 'ページ目を取得しました')
    if len(job_cards) != 21:
        break

today = datetime.date.today()
with open(today.strftime('%Y%m%d') + '.csv', 'w') as file:
    writer = csv.writer(file, lineterminator='\n')
    writer.writerows(csvlist)
    