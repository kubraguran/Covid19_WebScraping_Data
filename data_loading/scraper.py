import os
import re
import csv
import requests
from bs4 import BeautifulSoup
import pandas as pd 


CURRENT_DIR  = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(CURRENT_DIR)
DATA_DIR = os.path.join(BASE_DIR, 'data', 'raw')
CSV_FILE = os.path.join(DATA_DIR, 'covid_data.csv')


url = 'https://www.worldometers.info/coronavirus/'
page = requests.get(url)
soup = BeautifulSoup(page.text, 'lxml')

def clean_text(text):
    text = text.strip()
    text = re.sub(r'\s+',' ', text)
    return text if text else 'N/A'


table = soup.find('table', id = 'main_table_countries_today')
headers = table.find_all('th')[1:]
table_title =[]

def cleanDataTitle(data):
    for word in data:
        if word.text.strip() != '#':
            table_title.append(clean_text(word.get_text(separator=" ", strip=True)))

cleanDataTitle(headers)
df = pd.DataFrame(columns = table_title)


column_data = table.find_all('tr')

def cleanDataColumn(data):
    rows = []
    for row in data:
        row_data = row.find_all("td")
        if len(row_data) == len(table_title) + 1:
            rows.append([clean_text(td.text) for td in row_data[1:]])
    return pd.DataFrame(rows, columns = table_title)



df = cleanDataColumn(column_data)
print(df)
df.to_csv(CSV_FILE, index=False)
print(f"{CSV_FILE} has been uploaded")