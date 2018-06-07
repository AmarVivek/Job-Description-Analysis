import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import json

#url_template = "http://www.indeed.ca/jobs?q={}&l={}&start={}"
url_template="https://www.glassdoor.ca/Job/{}-{}-jobs-SRCH_IL.0,7_IC2275123_KO8,{}_IP{}.htm"
job_url_template = "https://ca.indeed.com/viewjob?jk={}"
max_results_per_job = 500 # Set this to a high-value (5000) to generate more results.
# Crawling more results, will also take much longer. First test your code on a small number of results and then expand.
i = 0
results = []
job_description = []
final_report = []
df_more = pd.DataFrame(columns=["Job Type","Title","Location","Company", "Job_Url"])
df_more_final = pd.DataFrame(columns=["Job Type","Title","Location","Company", "Job_Url","Job_Description"])
city = "Calgary"
pages=1
for job_type in set(['software-developer']):
    # Grab the results from the request (as above)
    start = 0
    job_length=len(job_type) + len(city) + 1
    print("Job Length : " + str(job_length))
    url = url_template.format(city,job_type,job_length,pages)
    # Append to the full set of results
    total_jobs = 0
    header = {"User-Agent": "my web scraping program."}
    try:
        html = requests.get(url, headers=header)
        soup = BeautifulSoup(html.content, 'html.parser')
        print(url)
        total_jobs_text = soup.find(class_="jobsCount").text.replace('\n','')
        total_jobs_list = re.findall('\d+', total_jobs_text)
        total_jobs = int(total_jobs_list[0])
        print("Running the loop for : " + str(job_type) + " .Total Jobs Found : " + str(total_jobs))
        num_pages = int(total_jobs)//30 + 1
        if num_pages > 25:
            num_pages = 25
    except:
        num_pages = 25
    statement = "For the role of " + str(job_type) + ", we found total of " + str(total_jobs) + " jobs!"
    final_report.append(statement)
    url = url_template.format(city,job_type,job_length,pages)
    print ("First Loop: " + url)
    html = requests.get(url,headers=header)
    soup = BeautifulSoup(html.content, 'html.parser', from_encoding="utf-8")
    k=0
    json_html = soup.find(type="application/ld+json")
    json_text = json_html.text
    datastore = json.loads(json_text)
    urllist = (datastore['itemListElement'])
    for url_item in urllist:
        url_dict = json.dumps(url_item)
        url_json = json.loads(url_dict)
        url = url_json['url']
        df_more = df_more.append({'Job Type': job_type, 'Job_Url': url}, ignore_index=True)

df_more.to_csv('Glassdoor_Project_OnlyURL.csv', encoding='utf-8')

for rows in df_more['Job_Url']:
    desc_html = requests.get(rows, headers=header)
    desc_soup = BeautifulSoup(desc_html.content, 'html.parser', from_encoding="utf-8")
    desc_json_html = desc_soup.find(type="application/ld+json")
    desc_json_text = desc_json_html.text.lstrip()
    desc_datastore = json.loads(desc_json_text, strict=False)
    title = (desc_datastore['title'])
    company = desc_datastore['hiringOrganization']['name']
    location = desc_datastore['jobLocation']['address']['addressLocality']
    description = desc_datastore['description'].replace('\n', ' ')
    df_more_final = df_more_final.append({'Title': title, 'Location': location,
                                          'Company': company, 'Job_Url': rows, 'Job_Description': description},
                                         ignore_index=True)

    if k % 200 == 0:
        print('Data has been scrapped for ' + str(k) + ' jobs for a total of ' + str(i) + ' jobs!')
    k += 1

df_more_final['Job Type'] = df_more['Job Type']
for rows in final_report:
    print(rows)

df_more_final.to_csv('Glassdoor_Project_withJD.csv', encoding='utf-8')