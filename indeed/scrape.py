import requests
from bs4 import BeautifulSoup
import time
import csv
import datetime

keyword = 'Webエンジニア' #キーワード
Work_location = '大阪府%20大阪市' #勤務地

csvlist = []
url_index = 'https://jp.indeed.com'
id = 1

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:58.0) Gecko/20100101 Firefox/58.0'}
headers['referer'] = 'https://www.google.co.jp'

for page in range(0, 20):
    url = f'https://jp.indeed.com/jobs?q={keyword}&l={Work_location}&start={page}0'
    res = requests.get(url,headers = headers)
    time.sleep(5)
    soup = BeautifulSoup(res.text, 'html.parser')

    job_cards = soup.find_all(class_='company')
    job_salarys = soup.find_all(class_='salaryText')
    job_card_heads = soup.find_all(class_='title')
    # job_urls = soup.find_all(class_='jobtitle')
    # print(len(job_urls))
    # print(job_cards)

    for (job_card, job_salary, job_card_head) in zip(job_cards, job_salarys, job_card_heads,):
        print([id, job_card.text.replace("\n"," "),job_salary.text.replace("\n"," ").replace(" ",""), job_card_head.text.replace("\n"," ")])
        csvlist.append([id, job_card.text.replace("\n"," "), job_salary.text.replace("\n"," ").replace(" ",""), job_card_head.text.replace("\n"," ")])
        id += 1
    print(str(page+1) + 'ページ目を取得しました')
    if len(job_cards) < 15:
        print(len(job_cards))
        break

today = datetime.date.today()
with open(today.strftime('%Y%m%d') + keyword + Work_location + '.csv', 'w') as file:
    writer = csv.writer(file, lineterminator='\n')
    writer.writerows(csvlist)

# url_detail = url_index + job_urls.get('href')
# print (url_detail)
# res2 = requests.get(url_detail, headers = headers)
# time.sleep(3)
# soup2 = BeautifulSoup(res2.text, 'html.parser')
# job_detail = soup2.find_all(class_='jobsearch-jobDescriptionText')
# print(job_detail)