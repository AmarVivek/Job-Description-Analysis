import urllib
import requests
import bs4
from bs4 import BeautifulSoup
import pandas as pd
from random import choice
import re

desktop_agents = [
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/602.2.14 (KHTML, like Gecko) Version/10.0.1 Safari/602.2.14',
    'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0']


def random_headers():
    return {'User-Agent': choice(desktop_agents),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'}

url_template = "http://www.indeed.ca/jobs?q={}&l={}&start={}"
job_url_template = "https://ca.indeed.com/viewjob?jk={}"
max_results_per_job = 500 # Set this to a high-value (5000) to generate more results.
# Crawling more results, will also take much longer. First test your code on a small number of results and then expand.
i = 0
results = []
job_description = []
final_report = []
df_more = pd.DataFrame(columns=["Job Type","Title","Location","Company","Salary", "Job_Url"])
city = ""
for job_type in set(['ai+machine+learning+developer', "backend+developer", "cloud+developer", "cyber+security+expert",
                     "data+scientist", "frontend+software+developer", 'full+stack+developer', "qa+engineer", "ux+ui+designer"]):
    # Grab the results from the request (as above)
    start = 0
    url = url_template.format(job_type, city, start)
    # Append to the full set of results
    total_jobs = 0
    try:
        html = requests.get(url, headers=random_headers())
        soup = BeautifulSoup(html.content, 'html.parser', from_encoding="utf-8")
        total_jobs = soup.find(id="searchCount").text.replace('\n', '').split('of')[1]
        print("Running the loop for : " + str(job_type) + " .Total Jobs Found : " + total_jobs)
        num_pages = int(total_jobs)//20 + 1
        if num_pages > 25:
            num_pages = 25
    except:
        try:
            html = requests.get(url, headers=random_headers())
            soup = BeautifulSoup(html.content, 'html.parser', from_encoding="utf-8")
            total_jobs = soup.find(id="searchCount").text.replace('\n', '').split('of')[1]
            print("Running the loop for : " + str(job_type) + " .Total Jobs Found : " + total_jobs)
            num_pages = int(total_jobs) // 20 + 1
            if num_pages > 25:
                num_pages = 25
        except:
            num_pages=25
    statement = "For the role of " + str(job_type) + ", we found total of " + str(total_jobs) + " jobs!"
    final_report.append(statement)
    for pages in range(0, num_pages):
        # Grab the results from the request (as above)
        url = url_template.format(job_type, city, start)
        start += 20
        #print(url)
        # Append to the full set of results
        html = requests.get(url, headers=random_headers())
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
                job_key = each.get('data-jk')
                job_url = job_url_template.format(job_key)
            except:
                job_url = None
            df_more = df_more.append({'Job Type':job_type,'Title':title, 'Location':location, 'Company':company, 'Salary':salary, 'Job_Url':job_url}, ignore_index=True)
            i += 1
            if i % 50 == 0:
                print('You have ' + str(i) + ' results. ' + str(df_more.dropna().drop_duplicates().shape[0]) + " of these are useful.")
#df_more.to_csv('Indeed_Project_withoutJD.csv', encoding='utf-8')
k=0
for rows in df_more['Job_Url']:
    html = requests.get(rows, headers=random_headers())
    soup = BeautifulSoup(html.content, 'html.parser', from_encoding="utf-8")
    try:
        description = soup.find('span', {'class':"summary" }).text.replace('\n', ' ')
    except:
        description = None
    if k % 200 == 0:
        print ('Data has been scrapped for ' + str(k) + ' jobs for a total of ' + str(i) + ' jobs!')
    job_description.append(description)
    k += 1

for rows in final_report:
    print(rows)

df_more["Job_Description"] = job_description
#df_more.to_csv('Indeed_Project_withJD.csv', encoding='utf-8')

#Just making sure that if any items were not listed due to issues in html parsing, they are addressed here
print("Restarting for Descriptions that were missed out!")
for index, row in df_more.iterrows():
    if pd.isnull(row['Job_Description']):
        html = requests.get(row['Job_Url'], headers=random_headers())
        soup = BeautifulSoup(html.content, 'html.parser', from_encoding="utf-8")
        try:
            description = soup.find('span', {'class': "summary"}).text.replace('\n', ' ')
        except:
            description = None
        if k % 2 == 0:
            print('Data has been scrapped for ' + str(k) + ' jobs for a total of ' + str(i) + ' jobs!')
        df_more.set_value(index, 'Job_Description',description)
        k += 1

print("Total Values Filled in the Second Iteration: " + str(k))

df_more.to_csv('Indeed_Project_withJDAll_National.csv', encoding='utf-8')