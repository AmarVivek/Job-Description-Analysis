from time import sleep
import requests
import bs4
from bs4 import BeautifulSoup
import pandas as pd
from random import choice
import re
from datetime import datetime

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


def get_indeed_jobs(job_set, url_template, job_url_template):
    max_results_per_job = 500 # Set this to a high-value (5000) to generate more results.
    # Crawling more results, will also take much longer. First test your code on a small number of results and then expand.
    i = 0
    results = []
    job_description = []
    final_report = []
    df_more = pd.DataFrame(columns=["Job Type","Title","Location","Company","Salary", "Job_Url"])
    city = ""
    for job_type in job_set:
        # Grab the results from the request (as above)
        start = 0
        i = 0
        url = url_template.format(job_type, city, start)
        # Append to the full set of results
        total_jobs = 0
        try:
            html = requests.get(url, headers=random_headers())
            soup = BeautifulSoup(html.content, 'html.parser', from_encoding="utf-8")
            #total_jobs = soup.find(id="searchCount").text.replace('\n', '').split('of')[1]
            total_jobs_text = soup.find(id="searchCount").text.replace('\n', '').split('of')[1]
            print(str(job_type) + str(total_jobs_text))
            total_jobs_list = re.findall('\d+', total_jobs_text)
            print (total_jobs_list , str(len(total_jobs_list)))
            if len(total_jobs_list) > 1:
                total_jobs = (int(total_jobs_list[0]) * 1000) + int(total_jobs_list[1])
            else:
                total_jobs = int(total_jobs_list[0])
            print("Running the loop for : " + str(job_type) + " .Total Jobs Found : " + str(total_jobs))
            num_pages = int(total_jobs)//20 + 1
        except:
            try:
                html = requests.get(url, headers=random_headers())
                soup = BeautifulSoup(html.content, 'html.parser', from_encoding="utf-8")
                # total_jobs = soup.find(id="searchCount").text.replace('\n', '').split('of')[1]
                total_jobs_text = soup.find(id="searchCount").text.replace('\n', '').split('of')[1]
                print(str(job_type) + str(total_jobs_text))
                total_jobs_list = re.findall('\d+', total_jobs_text)
                print(total_jobs_list, str(len(total_jobs_list)))
                if len(total_jobs_list) > 1:
                    total_jobs = (int(total_jobs_list[0]) * 1000) + int(total_jobs_list[1])
                else:
                    total_jobs = int(total_jobs_list[0])
                print("Running the loop for : " + str(job_type) + " .Total Jobs Found : " + str(total_jobs))
                num_pages = int(total_jobs) // 20 + 1
            except:
                continue
        ##
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
                if i%200 ==0:
                    sleep(5)
                    print (str(i) + " jobs extracted out of " + str(total_jobs) + " for the role of " + str(job_type))
        print ("For the job of " + str(job_type) + ", a total of " + str(i) + " jobs were extracted in total!")
    #df_more.to_csv('Indeed_Project_withoutJD.csv', encoding='utf-8')
    print ("Total Jobs written in this run: " +str(len(df_more)))
    return df_more

def get_indeed_data(out_file_name):
    #job_master_set = set(['software+developer','software+engineer','data+scientist','ux+ui+designer','fullstack+developer',
    #            'ai+machine+learning+developer','project+manager',"electrical+engineer", "qa+engineer",
     #                "cloud+developer","business+development+manager","frontend+software+developer",
    #                 "business+analyst","backend+developer","cybersecurity+expert"])
    job_set = set(['software+developer','software+engineer','project+manager',"electrical+engineer", "business+development+manager","business+analyst"])
    url_template = "http://www.indeed.ca/jobs?q={}&l={}&start={}"
    job_url_template = "https://ca.indeed.com/viewjob?jk={}"
    df_indeed = get_indeed_jobs(job_set, url_template, job_url_template)
    df_indeed_uniq = df_indeed.drop_duplicates(subset=['Job_Description'])
    df_indeed_uniq.to_csv(out_file_name, encoding='utf-8')
    return None

if __name__ == "__main__":
    start_time = datetime.now()
    get_indeed_data("Indeed_National_Data.csv")
    #n_grams_wordCloud("C:/Users/a.vivek/PycharmProjects/Calgary/ngram2.py",'utf-8', n_filter=2, n=3)
    #with open("output.csv", 'w',newline='') as resultFile:
    #    wr = csv.writer(resultFile, dialect='excel')
    #    wr.writerow(['Ngram_Freq','MI','Ngram_Prob','Count','Ngram'])
    #    wr.writerows(s)
    end_time = datetime.now()
    print('Duration: {}'.format(end_time - start_time))