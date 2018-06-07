import urllib
import requests
import bs4
from bs4 import BeautifulSoup
import pandas as pd
import re
import json

url_template="https://stackoverflow.com/jobs?sort=i&q={}&l={}"
max_results_per_job = 500 # Set this to a high-value (5000) to generate more results.
# Crawling more results, will also take much longer. First test your code on a small number of results and then expand.
i = 0
results = []
job_description = []
final_report = []
df_more = pd.DataFrame(columns=["Source","Job Type","Title","Location","Company", "Job_Url","Job_Description"])
city = "calgary"
source="StackOverFlow"
for job_type in set(['software+developer','software+engineer','data+scientist','ux+ui+designer','fullstack+developer',
                'ai+machine+learning+developer','project+manager',"electrical+engineer", "qa+engineer",
                     "cloud+developer","business+development+manager","frontend+software+developer",
                     "business+analyst","backend+developer","cybersecurity+expert"]):
    # Grab the results from the request (as above)
    start = 0
    url = url_template.format(job_type,city)
    # Append to the full set of results
    total_jobs = 0
    try:
        html = requests.get(url)
        soup = BeautifulSoup(html.content, 'html.parser')
        total_jobs_text = soup.find(class_="description").text.replace('\n', '')
        total_jobs_list = re.findall('\d+', total_jobs_text)
        total_jobs = int(total_jobs_list[0])
        print("Running the loop for : " + str(job_type) + " .Total Jobs Found : " + str(total_jobs))
        num_pages = int(total_jobs)//20 + 1
        if num_pages > 25:
            num_pages = 25
    except:
        try:
            html = requests.get(url)
            soup = BeautifulSoup(html.content, 'html.parser')
            total_jobs_text = soup.find(class_="description").text.replace('\n', '')
            total_jobs_list = re.findall('\d+', total_jobs_text)
            total_jobs = int(total_jobs_list[0])
            print("Running the loop for : " + str(job_type) + " .Total Jobs Found : " + str(total_jobs))
            num_pages = int(total_jobs) // 20 + 1
            if num_pages > 25:
                num_pages = 25
        except:
            num_pages = 25
    statement = "For the role of " + str(job_type) + ", we found total of " + str(total_jobs) + " jobs!"
    final_report.append(statement)
    for each in soup.find(class_='listResults'):
        try:
            href = each.find(class_='job-link').get('href')
            job_url = "https://stackoverflow.com" + href
            df_more = df_more.append({'Job Type': job_type, 'Job_Url': job_url, 'Source':source}, ignore_index=True)
            i +=1
            if i % 50 == 0:
                print('You have ' + str(i) + ' results. ' + str(df_more.dropna().drop_duplicates().shape[0]) + " of these are useful.")
        except:
            job_url = None

df_more.to_csv('StackOverflow_Project_OnlyURL.csv', encoding='utf-8')

k=0
for index, row in df_more.iterrows():
    html = requests.get(row['Job_Url'])
    soup = BeautifulSoup(html.content, 'html.parser', from_encoding="utf-8")
    try:
        json_html = soup.find(type="application/ld+json")
        json_text = json_html.text
        datastore = json.loads(json_text)
        company = (datastore['hiringOrganization']['name'])
        location = (datastore['jobLocation'][0]['address']['addressLocality'])
        description = BeautifulSoup(datastore['description'], 'html.parser').text.replace('\n', ' ')
        title = (datastore['title'])
        df_more.set_value(index, 'Job_Description', description)
        df_more.set_value(index, 'Company', company)
        df_more.set_value(index, 'Location', location)
        df_more.set_value(index, 'Title', title)
        if k % 40 == 0:
            print ('Data has been scrapped for ' + str(k) + ' jobs for a total of ' + str(i) + ' jobs!')
        k += 1
    except:
        description = None

for rows in final_report:
    print(rows)

df_more.to_csv('StackOverflow_Project_withJD.csv', encoding='utf-8')