import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import json
from time import sleep
from random import choice

url_template = "https://www.glassdoor.ca/Job/{}-jobs-SRCH_KO0,{}_IP{}.htm"
job_url_template = "https://www.glassdoor.ca"
max_results_per_job = 500  # Set this to a high-value (5000) to generate more results.
# Crawling more results, will also take much longer. First test your code on a small number of results and then expand.
i = 0
results = []
job_description = []
final_report = []
error_report = []
df_more = pd.DataFrame(columns=["Job Type", "Title", "Location", "Company", "Job_Url"])
df_more_final = pd.DataFrame(columns=["Job Type", "Title", "Location", "Company", "Job_Url", "Job_Description"])

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

for job_type in set(['ai-machine-learning-developer', "backend-developer", "cloud-developer", "cyber-security-expert",
                     "data-scientist", "frontend-software-developer", 'full-stack-developer', "qa-engineer", "ux-ui-designer"]):
    # Grab the results from the request (as above)
    start = 0
    job_length=len(job_type)
    print("Job Length : " + str(job_length))
    url = url_template.format(job_type,job_length,1)
    print (url)
    # Append to the full set of results
    total_jobs = 0
    try:
        html = requests.get(url, headers=random_headers())
        sleep(5)
        soup = BeautifulSoup(html.content, 'html.parser')
        total_jobs_text = soup.find(class_="jobsCount").text.replace('\n','')
        print (str(job_type) + str(total_jobs_text))
        total_jobs_list = re.findall('\d+', total_jobs_text)
        if len(total_jobs_list) > 1:
            total_jobs = (int(total_jobs_list[0])*1000) + int(total_jobs_list[1])
        else:
            total_jobs = int(total_jobs_list[0])
        print("Running the loop for : " + str(job_type) + " .Total Jobs Found : " + str(total_jobs))
        num_pages = int(total_jobs)//30 + 1
        if num_pages > 20:
            num_pages = 20
    except:
        try:
            html = requests.get(url, headers=random_headers())
            sleep(5)
            soup = BeautifulSoup(html.content, 'html.parser')
            total_jobs_text = soup.find(class_="jobsCount").text.replace('\n', '')
            print(str(job_type) + str(total_jobs_text))
            total_jobs_list = re.findall('\d+', total_jobs_text)
            if len(total_jobs_list) > 1:
                total_jobs = (int(total_jobs_list[0]) * 1000) + int(total_jobs_list[1])
            else:
                total_jobs = int(total_jobs_list[0])
            print("Running the loop for : " + str(job_type) + " .Total Jobs Found : " + str(total_jobs))
            num_pages = int(total_jobs) // 30 + 1
            if num_pages > 20:
                num_pages = 20
        except Exception as e:
            print ("Error getting total jobs for the url : " + str(url) + " and the error is : " + str(e))
            num_pages = 0
    statement = "For the role of " + str(job_type) + ", we found total of " + str(total_jobs) + " jobs!"
    final_report.append(statement)
    for pages in range(1, num_pages):
        try:
            url = url_template.format(job_type, job_length, pages)
            html = requests.get(url, headers=random_headers())
            sleep(5)
            soup = BeautifulSoup(html.content, 'html.parser', from_encoding="utf-8")
            k = 0
            for each in soup.find_all('td', {'class': 'job_title'}):
                href_area = each.find('a', {'class': 'jobLink'})
                href = href_area.get('href')
                job_url = job_url_template + href
                df_more = df_more.append({'Job Type': job_type, 'Job_Url': job_url}, ignore_index=True)
                i += 1
        except:
            try:
                url = url_template.format(job_type, job_length, pages)
                html = requests.get(url, headers=random_headers())
                sleep(5)
                soup = BeautifulSoup(html.content, 'html.parser', from_encoding="utf-8")
                k = 0
                for each in soup.find_all('td', {'class': 'job_title'}):
                    href_area = each.find('a', {'class': 'jobLink'})
                    href = href_area.get('href')
                    job_url = job_url_template + href
                    df_more = df_more.append({'Job Type': job_type, 'Job_Url': job_url}, ignore_index=True)
                    i += 1
            except:
                error = "For the role of " + str(job_type) + ", we did not get data on the following url page : " + str(url)
                error_report.append(error)
                print (error)

#df_more.to_csv('Glassdoor_Project_OnlyURL.csv', encoding='utf-8')

for index, row in df_more.iterrows():
    try:
        desc_html = requests.get(row['Job_Url'], headers=random_headers())
        sleep(5)
        desc_soup = BeautifulSoup(desc_html.content, 'html.parser', from_encoding="utf-8")
        desc_json_html = desc_soup.find(type="application/ld+json")
        desc_json_text = desc_json_html.text.lstrip()
        desc_datastore = json.loads(desc_json_text, strict=False)
        title = (desc_datastore['title'])
        company = desc_datastore['hiringOrganization']['name']
        location = desc_datastore['jobLocation']['address']['addressLocality']
        description = desc_datastore['description'].replace('\n', ' ')
        df_more.at[index, 'Title'] = title
        df_more.at[index, 'Location'] = location
        df_more.at[index, 'Company'] = company
        df_more.at[index, 'Job_Description'] = description
        #df_more.set_value(index,'Title', title)
        #df_more.set_value(index, 'Location', location)
        #df_more.set_value(index, 'Company', company)
        #df_more.set_value(index, 'Job_Description', description)

        if k % 50 == 0:
            print('Data has been scrapped for ' + str(k) + ' jobs for a total of ' + str(i) + ' jobs!')
            sleep(5)
        k += 1
    except:
        sleep(5)
        try:
            desc_html = requests.get(row['Job_Url'], headers=random_headers())
            sleep(5)
            desc_soup = BeautifulSoup(desc_html.content, 'html.parser', from_encoding="utf-8")
            desc_json_html = desc_soup.find(type="application/ld+json")
            desc_json_text = desc_json_html.text.lstrip()
            desc_datastore = json.loads(desc_json_text, strict=False)
            title = (desc_datastore['title'])
            company = desc_datastore['hiringOrganization']['name']
            location = desc_datastore['jobLocation']['address']['addressLocality']
            description = desc_datastore['description'].replace('\n', ' ')
            df_more.set_value(index, 'Title', title)
            df_more.set_value(index, 'Location', location)
            df_more.set_value(index, 'Company', company)
            df_more.set_value(index, 'Job_Description', description)

            if k % 50 == 0:
                print('Data has been scrapped for ' + str(k) + ' jobs for a total of ' + str(i) + ' jobs!')
                sleep(5)
            k += 1
        except:
            error = ("Error Occurred for URL : " + str(row['Job_Url']))
            error_report.append(error)

for rows in final_report:
    print(rows)

for rows in error_report:
    print(rows)

df_more.to_csv('Glassdoor_Project_withJD_National.csv', encoding='utf-8')