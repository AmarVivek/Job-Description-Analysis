import urllib
import requests
import bs4
from bs4 import BeautifulSoup
import pandas as pd
import re
import json

url_template="http://www.calgaryjobboard.ca/index.php?action=search&order_by=&ord=&2=&5={}&102%5B%5D=163&14=&search=Find"
max_results_per_job = 500 # Set this to a high-value (5000) to generate more results.
# Crawling more results, will also take much longer. First test your code on a small number of results and then expand.
i = 0
results = []
job_description = []
final_report = []
df_more = pd.DataFrame(columns=["Job Type","Title","Location","Company", "Job_Url"])
df_more_final = pd.DataFrame(columns=["Job Type","Title","Location","Company", "Job_Url","Job_Description"])
city = "calgary"
for job_type in set(['software+developer','software+engineer','data+scientist','ux+ui+designer','fullstack+developer',
                'ai+machine+learning+developer','project+manager',"electrical+engineer", "qa+engineer",
                     "cloud+developer","business+development+manager","frontend+software+developer",
                     "business+analyst","backend+developer","cybersecurity+expert"]):
    # Grab the results from the request (as above)
    start = 0
    url = url_template.format(job_type)
    # Append to the full set of results
    total_jobs = 0
    try:
        html = requests.get(url)
        soup = BeautifulSoup(html.content, 'html.parser')
        total_jobs_text = soup.find(class_="job_listing_count").text.replace('\n', '')
        total_jobs_list = re.findall('\d+', total_jobs_text)
        total_jobs = int(total_jobs_list[0])
        print("Running the loop for : " + str(job_type) + " .Total Jobs Found : " + str(total_jobs))
        #num_pages = int(total_jobs)//20 + 1
        #if num_pages > 25:
        #    num_pages = 25
    except:
        total_jobs=0
    statement = "For the role of " + str(job_type) + ", we found total of " + str(total_jobs) + " jobs!"
    final_report.append(statement)
    if total_jobs == 0:
        continue
    for each in soup.find_all('a', {'class':'job_list_title'}):
        try:
            href = each.get('href')
            #href = each.find(class_='job_list_title').get('href')
            job_url = "http://www.calgaryjobboard.ca" + href
            df_more = df_more.append({'Job Type': job_type, 'Job_Url': job_url}, ignore_index=True)
            i +=1
            if i % 50 == 0:
                print('You have ' + str(i) + ' results. ' + str(df_more.dropna().drop_duplicates().shape[0]) + " of these are useful.")
        except:
            job_url = None

df_more.to_csv('CalgaryJobBoard_Project_OnlyURL.csv', encoding='utf-8')

k=0
#for rows in df_more['Job_Url']:
#rows= "http://www.calgaryjobboard.ca/index.php?post_id=96134&action=search&2=software+developer&102%5B%5D=163"
for rows in df_more['Job_Url']:
    html = requests.get(rows)
    soup = BeautifulSoup(html.content, 'html.parser', from_encoding="utf-8")
    try:
        title = ' '
        company = ' '
        description = ' '
        location = ' '
        title = soup.find(class_="jobTitle").text.replace('\n', '')
        company = soup.find(class_='empTitle').text.replace('\n','')
        if company == '':
            company = 'Confidential'
        location_found = 0
        description = soup.find(id = "jd").text.replace('\n',' ')
        for each in soup.find_all(): #.find_all('td', {'class':'dynamic_form'}):
            #print(each)
            if each.text.replace('\n','').lstrip() == "Location":
                location_found = 1
            if location_found==1 and each.get('class')[0] == 'dynamic_form_value':
                location = (each.text.replace('\n','').lstrip())
                break
        df_more_final = df_more_final.append({'Job Type': job_type, 'Title': title, 'Location':location,
                                  'Company':company,'Job_Url': rows, 'Job_Description':description}, ignore_index=True)
        if k % 200 == 0:
            print ('Data has been scrapped for ' + str(k) + ' jobs for a total of ' + str(i) + ' jobs!')
        k += 1
    except:
        description = None

df_more_final['Job Type'] = df_more['Job Type']
for rows in final_report:
    print(rows)

df_more_final.to_csv('CalgaryJobBoard_Project_withJD.csv', encoding='utf-8')

