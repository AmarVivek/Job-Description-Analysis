import urllib
import requests
import bs4
from bs4 import BeautifulSoup
import pandas as pd
import re

df_read = pd.read_csv("Indeed_Project_withJDAll.csv")
k=0
i=len(df_read)
print("Restarting for Descriptions that were missed out!")
for index, row in df_read.iterrows():
    if pd.isnull(row['Job_Description']):
        html = requests.get(row['Job_Url'])
        soup = BeautifulSoup(html.content, 'html.parser', from_encoding="utf-8")
        try:
            description = soup.find('span', {'class': "summary"}).text.replace('\n', '')
        except:
            description = None
        if k % 2 == 0:
            print('Data has been scrapped for ' + str(k) + ' jobs for a total of ' + str(i) + ' jobs!')
        df_read.set_value(index, 'Job_Description',description)
        k += 1

print("Total Values Filled : " + str(k))

# Change the file name to the target file name needed below.
#df_read.to_csv('Indeed_Project_withJDAll.csv', encoding='utf-8')
