import requests
from bs4 import BeautifulSoup
import time
import csv
import datetime
import pandas as pd

keyword = 'Laravel' #キーワード
key = 'cauhcr3rcyngf4hwvnuj' #都道府県(大阪) key = 'fsv0rltm6p1g8pvv6vei'（東京）

csvlist = []
url_index = 'https://www.green-japan.com'
id = 1

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:58.0) Gecko/20100101 Firefox/58.0'}
headers['referer'] = 'https://www.google.co.jp'

for page in range(1,10):
    url = f'https://www.green-japan.com/search_key/01?key={key}&keyword={keyword}&page={page}'
    res = requests.get(url,headers)
    time.sleep(5)

    soup = BeautifulSoup(res.text, 'html.parser')
    # print(soup.prettify())

    job_cards = soup.find_all(class_='card-info__detail-area__box__title')
    job_salarys = soup.find_all(class_='job-offer-meta-tags')
    job_card_heads = soup.find_all(class_='card-info__heading-area__title')
    job_urls = soup.find_all(class_='js-search-result-box card-info')
    # print(len(job_salarys))
    # break

    for (job_card, job_salary, job_card_head, job_url) in zip(job_cards, job_salarys, job_card_heads, job_urls):
        print([id, job_card.text,job_salary.li.text.replace("\n"," ").replace(" ",""), job_card_head.text, url_index + job_url.get('href')])
        csvlist.append([job_card.text, job_salary.li.text.replace("\n"," ").replace(" ",""), job_card_head.text, url_index + job_url.get('href')])
        id += 1
    print(str(page) + 'ページ目を取得しました')
    if len(job_cards) != 10:
        break

today = datetime.date.today()
with open(today.strftime('%Y%m%d') + '_green_' + keyword + '.csv', 'w', encoding='utf-8-sig') as file:
    writer = csv.writer(file, lineterminator='\n')
    writer.writerows(csvlist)

columns1 = ["company", "salary", "title"]
df = pd.DataFrame(data=csvlist, columns=columns1)
print(df.duplicated(subset=['company']).sum())