import urllib
import requests
import bs4
from bs4 import BeautifulSoup
import pandas as pd
import re

url_template = "http://www.indeed.ca/jobs?q=data+scientist+%2420%2C000&l={}&start={}"
job_url_template = "https://ca.indeed.com/viewjob?jk={}"
max_results_per_job = 20 # Set this to a high-value (5000) to generate more results.
# Crawling more results, will also take much longer. First test your code on a small number of results and then expand.
i = 0
results = []
job_description = []
df_more = pd.DataFrame(columns=["Title","Location","Company","Salary", "Job_Url"])
city = "Calgary"
for start in range(0, max_results_per_job, 10):
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
        try:
            #jobKey = each.find(class_='result').get('data-jk').text
            #job_URLs = [each.find(class_='jobtitle').get('href')]
            job_key = each.get('data-jk')
            job_url = job_url_template.format(job_key)
        except:
            job_url="None"
        df_more = df_more.append({'Title':title, 'Location':location, 'Company':company, 'Salary':salary, 'Job_Url':job_url}, ignore_index=True)
        i += 1
        if i % 20 == 0:
            print('You have ' + str(i) + ' results. ' + str(df_more.dropna().drop_duplicates().shape[0]) + " of these are useful.")

k=0
for rows in df_more['Job_Url']:
    html = requests.get(rows)
    soup = BeautifulSoup(html.content, 'html.parser', from_encoding="utf-8")
    try:
        description = soup.find('span', {'class':"summary" }).text.replace('\n', '')
    except:
        description = 'None'
    job_description.append(description)
    k += 1

df_more["Job_Descrption"] = job_description
df_more.to_csv('Indeed_Project_test.csv', encoding='utf-8')