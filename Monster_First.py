import urllib
import requests
import bs4
from bs4 import BeautifulSoup
import pandas as pd
import re
from random import choice
from time import sleep
import json

url_template = "https://www.monster.ca/jobs/search/?q={}&where={}&stpage=1&page={}"
job_url_template = "https://ca.indeed.com/viewjob?jk={}"
max_results_per_job = 500 # Set this to a high-value (5000) to generate more results.
# Crawling more results, will also take much longer. First test your code on a small number of results and then expand.
i = 0
results = []
job_description = []
final_report = []
df_more = pd.DataFrame(columns=["Job Type","Title","Location","Company","Salary", "Job_Url"])
city = "Calgary"
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

for job_type in set(['data+scientist']):
    # Grab the results from the request (as above)
    start = 1
    url = url_template.format(job_type, city, start)
    print(url)
    # Append to the full set of results
    total_jobs = 0
    html = requests.get(url, headers=random_headers())
    soup = BeautifulSoup(html.content, 'html.parser', from_encoding="utf-8")
    print (soup)
    total_jobs = soup.find('p', {'class':"title"}).text.replace('\n', '')
    total_jobs = int(re.findall('\d+', total_jobs)[0])
    print("Running the loop for : " + str(job_type) + " .Total Jobs Found : " + str(total_jobs))
    num_pages = int(total_jobs)//25 + 1
    if num_pages > 20:
        num_pages = 20
    statement = "For the role of " + str(job_type) + ", we found total of " + str(total_jobs) + " jobs!"
    final_report.append(statement)
    url = url_template.format(job_type, city, start)
    html = requests.get(url, headers=random_headers())
    sleep(5)
    soup = BeautifulSoup(html.content, 'html.parser', from_encoding="utf-8")
    k = 0
    soup_json = soup.find(id = 'ResultsScrollable')
    json_html_area = soup_json.find(type = 'application/ld+json')
    json_html_area_text = json_html_area.text.lstrip()
    json_area = json.loads(json_html_area_text, strict=False)
    print(json_area)
    itemList = json_area['itemListElement']
    for json_url_list in itemList:
        print (json_url_list)
        #url_area = json.loads(json_url_list, strict=False)
        #job_link_url = url_area['url']
        #print (job_link_url)
