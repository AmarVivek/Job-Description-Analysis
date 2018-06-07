URL = "http://www.indeed.com/jobs?q=data+scientist+%2420%2C000&l=New+York&start=10"
import urllib
import requests
import bs4
from bs4 import BeautifulSoup
import pandas as pd
import re

def parse(url):
    html = requests.get(url)
    soup = BeautifulSoup(html.content, 'html.parser', from_encoding="utf-8")
    df = pd.DataFrame(columns=["Title","Location","Company","Salary", "Synopsis"])
    for each in soup.find_all(class_= "result" ):
        try:
            title = each.find(class_='jobtitle').text.replace('\n', '')
        except:
            title = 'None'
        try:
            location = each.find('span', {'class':"location" }).text.replace('\n', '')
        except:
            location = 'None'
        try:
            company = each.find(class_='company').text.replace('\n', '')
        except:
            company = 'None'
        try:
            salary = each.find('span', {'class':'no-wrap'}).text
        except:
            salary = 'None'
        synopsis = each.find('span', {'class':'summary'}).text.replace('\n', '')
        df = df.append({'Title':title, 'Location':location, 'Company':company, 'Salary':salary, 'Synopsis':synopsis}, ignore_index=True)
    return df

YOUR_CITY = 'Washington%2C+DC'

url_template = "http://www.indeed.com/jobs?q=data+scientist+%2420%2C000&l={}&start={}"
max_results_per_city = 2000 # Set this to a high-value (5000) to generate more results.
# Crawling more results, will also take much longer. First test your code on a small number of results and then expand.
i = 0
results = []
df_more = pd.DataFrame(columns=["Title","Location","Company","Salary", "Synopsis"])
for city in set(['New+York', 'Chicago', 'San+Francisco', 'Austin', 'Seattle',
    'Los+Angeles', 'Philadelphia', 'Atlanta', 'Dallas', 'Pittsburgh',
    'Portland', 'Phoenix', 'Denver', 'Houston', 'Miami', YOUR_CITY,
    'Charlottesville', 'Richmond', 'Baltimore', 'Harrisonburg', 'San+Antonio', 'San+Diego', 'San+Jose'
    'Austin', 'Jacksonville', 'Indianapolis', 'Columbus', 'Fort+Worth', 'Charlotte', 'Detroit', 'El+Paso',
    'Memphis', 'Boston', 'Nashville', 'Louisville', 'Milwaukee', 'Las+Vegas', 'Albuquerque', 'Tucson',
    'Fresno', 'Sacramento', 'Long+Beach', 'Mesa', 'Virginia+Beach', 'Norfolk', 'Atlanta', 'Colorado+Springs',
    'Raleigh', 'Omaha', 'Oakland', 'Tulsa', 'Minneapolis', 'Cleveland', 'Wichita', 'Arlington', 'New+Orleans',
    'Bakersfield', 'Tampa', 'Honolulu', 'Anaheim', 'Aurora', 'Santa+Ana', 'Riverside', 'Corpus+Christi', 'Pittsburgh',
    'Lexington', 'Anchorage', 'Cincinnati', 'Baton+Rouge', 'Chesapeake', 'Alexandria', 'Fairfax', 'Herndon',
    'Reston', 'Roanoke']):
    for start in range(0, max_results_per_city, 10):
        # Grab the results from the request (as above)
        url = url_template.format(city, start)
        # Append to the full set of results
        html = requests.get(url)
        soup = BeautifulSoup(html.content, 'html.parser', from_encoding="utf-8")
        for each in soup.find_all(class_= "result" ):
            try:
                title = each.find(class_='jobtitle').text.replace('\n', '')
            except:
                title = None
            try:
                location = each.find('span', {'class':"location" }).text.replace('\n', '')
            except:
                location = None
            try:
                company = each.find(class_='company').text.replace('\n', '')
            except:
                company = None
            try:
                salary = each.find('span', {'class':'no-wrap'}).text
            except:
                salary = None
            try:
                synopsis = each.find('span', {'class':'summary'}).text.replace('\n', '')
            except:
                synopsis = None
            df_more = df_more.append({'Title':title, 'Location':location, 'Company':company, 'Salary':salary, 'Synopsis':synopsis}, ignore_index=True)
            i += 1
            if i % 1000 == 0:  # Ram helped me build this counter to see how many. You can visibly see Ram's vernacular in the print statements.
                print('You have ' + str(i) + ' results. ' + str(df_more.dropna().drop_duplicates().shape[0]) + " of these aren't rubbish.")

df_more.to_csv('Indeed_Project_3_df_more_long_not_cleaned.csv', encoding='utf-8')