import pandas as pd

readcsv = '20210816_indeed_Webエンジニア大阪府%20大阪市.csv' # csvfileを指定する

columns1 = ["id", "company", "salary", "title"]
df = pd.read_csv(readcsv, encoding="cp932", names=columns1)
print(df.duplicated(subset=['company']).value_counts())
df.drop_duplicates(subset=['company'], inplace=True)
print(df)
df.to_csv('drop_duplicates' + readcsv,encoding='utf-8-sig')