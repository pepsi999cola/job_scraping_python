import requests
from bs4 import BeautifulSoup
import time
import csv
import datetime
import pandas as pd

keyword = 'Webエンジニア' #キーワード
Work_location = '大阪府%20大阪市' #勤務地
EXCLUSION = ''


csvlist = []
url_index = 'https://jp.indeed.com'
id = 1

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:58.0) Gecko/20100101 Firefox/58.0'}
headers['referer'] = 'https://www.google.co.jp'

for page in range(0, 3):
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
        csvlist.append([job_card.text.replace("\n"," "), job_salary.text.replace("\n"," ").replace(" ",""), job_card_head.text.replace("\n"," ")])
        id += 1
    print(str(page+1) + 'ページ目を取得しました')
    if len(job_cards) < 15:
        print(len(job_cards))
        break
# print(csvlist)
today = datetime.date.today()
with open(today.strftime('%Y%m%d') + '_indeed_' + keyword + Work_location + '.csv', 'w') as file:
    writer = csv.writer(file, lineterminator='\n')
    writer.writerows(csvlist)


# index1 = ["Row1", "Row2", "Row3", "Row4"]
columns1 = ["company", "salary", "title"]
df = pd.DataFrame(data=csvlist, columns=columns1)
# print(df1)
print(df.duplicated(subset=['company']).sum())
df.drop_duplicates(subset=['company'], inplace=True)
# print(df)
df.to_csv(today.strftime('%Y%m%d') + '_duplicated' + '_indeed_' + keyword + Work_location + '.csv', encoding='utf-8-sig')

#companyからEXCLUSIONする
print(df[df['company'].str.contains(EXCLUSION)])
df[~df['company'].str.contains(EXCLUSION)].to_csv(today.strftime('%Y%m%d') + '_best' + '_indeed_' + keyword + Work_location + '.csv', encoding='utf-8-sig')