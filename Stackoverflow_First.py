import urllib
import requests
import bs4
from bs4 import BeautifulSoup
import pandas as pd
import re

url_template="https://stackoverflow.com/jobs?sort=i&q={}&l={}"
max_results_per_job = 500 # Set this to a high-value (5000) to generate more results.
# Crawling more results, will also take much longer. First test your code on a small number of results and then expand.
i = 0
results = []
job_description = []
final_report = []
df_more = pd.DataFrame(columns=["Job Type","Title","Location","Company", "Job_Url"])
city = "calgary"
for job_type in set(['software+developer']):
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
    for each in soup.find_all(class_='listResults'):
        #print(each)
        try:
            title = each.find(class_='job-link').get('title')
            df_more = df_more.append({'Job Type': job_type, 'Title': title})
            #print(title)
        except:
            title = None
    for each in soup.find_all(class_='listResults'):
        try:
            location = each.find(class_='fc-black-700 fs-body2').text.replace('\n', '').split(',')[0]
            #print(location)
        except:
            location = None
    for each in soup.find_all(class_='listResults'):
        try:
            company = each.find(class_='fc-black-700 fs-body2').text.splitlines()[1].strip(' ')
            #print(company)
        except:
            company = None
    for each in soup.find_all(class_='listResults'):
        try:
            href = each.find(class_='job-link').get('href')
            job_url = "https://stackoverflow.com/" + href
        except:
            job_url = None
    if title == None and location == None and company == None and job_url == None:
        k=0
    else:
        df_more = df_more.append(
            {'Job Type': job_type, 'Title': title, 'Location': location, 'Company': company,
             'Job_Url': job_url}, ignore_index=True)
        i += 1

df_more.to_csv('StackOverflow_Project_withoutJD.csv', encoding='utf-8')
