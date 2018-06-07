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

def get_indeed_count(job_set,city):
    url_template = "http://www.indeed.ca/jobs?q={}&l={}&start={}"
    df_more = pd.DataFrame(columns=["Job Type", "Count", "Source"])
    source = "Indeed"
    for job_type in job_set:
        # Grab the results from the request (as above)
        start = 0
        job_type_clean = job_type.replace('+',' ')
        i = 0
        url = url_template.format(job_type, city.lower(), start)
        html = requests.get(url, headers=random_headers())
        soup = BeautifulSoup(html.content, 'html.parser', from_encoding="utf-8")
        total_jobs_text = soup.find(id="searchCount").text.replace('\n', '').split('of')[1]
        total_jobs_list = re.findall('\d+', total_jobs_text)
        if len(total_jobs_list) > 1:
            total_jobs = (int(total_jobs_list[0]) * 1000) + int(total_jobs_list[1])
        else:
            total_jobs = int(total_jobs_list[0])
        print("In " + str(source) + " For : " + str(job_type_clean) + ". Total Jobs Found : " + str(total_jobs))
        df_more = df_more.append({'Job Type': job_type_clean, 'Count': total_jobs, 'Source': source}, ignore_index=True)
    return df_more

def get_glassdoor_count(job_set, city):
    url_template = "https://www.glassdoor.ca/Job/{}-{}-jobs-SRCH_IL.0,7_IC2275123_KO8,{}_IP{}.htm"
    source = "Glassdoor"
    df_more = pd.DataFrame(columns=["Job Type", "Count", "Source"])
    for job_type in job_set:
        job_type_clean = job_type.replace('-', ' ')
        job_length = len(job_type) + len(city) + 1
        url = url_template.format(city.lower(),job_type, job_length, 1)
        html = requests.get(url, headers=random_headers())
        soup = BeautifulSoup(html.content, 'html.parser')
        total_jobs_text = soup.find(class_="jobsCount").text.replace('\n', '')
        total_jobs_list = re.findall('\d+', total_jobs_text)
        if len(total_jobs_list) > 1:
            total_jobs = (int(total_jobs_list[0]) * 1000) + int(total_jobs_list[1])
        else:
            total_jobs = int(total_jobs_list[0])
        print("In " + str(source) + " For : " + str(job_type_clean) + ". Total Jobs Found : " + str(total_jobs))
        df_more = df_more.append({'Job Type': job_type_clean, 'Count': total_jobs, 'Source': source}, ignore_index=True)
    return df_more

def get_stackoverflow_count(job_set, city):
    url_template = "https://stackoverflow.com/jobs?sort=i&q={}&l={}"
    source = "StackOverFlow"
    df_more = pd.DataFrame(columns=["Job Type", "Count", "Source"])
    for job_type in job_set:
        job_type_clean = job_type.replace('+', ' ')
        url = url_template.format(job_type, city)
        html = requests.get(url, headers=random_headers())
        soup = BeautifulSoup(html.content, 'html.parser')
        total_jobs_text = soup.find(class_="description").text.replace('\n', '')
        total_jobs_list = re.findall('\d+', total_jobs_text)
        if len(total_jobs_list) > 1:
            total_jobs = (int(total_jobs_list[0]) * 1000) + int(total_jobs_list[1])
        else:
            total_jobs = int(total_jobs_list[0])
        print("In " + str(source) + " For : " + str(job_type_clean) + ". Total Jobs Found : " + str(total_jobs))
        df_more = df_more.append({'Job Type': job_type_clean, 'Count': total_jobs, 'Source': source}, ignore_index=True)
    return df_more

def get_monster_count(job_set, city):
    url_template = "https://www.monster.ca/jobs/search/?q={}&where={}"
    source = "Monster"
    df_more = pd.DataFrame(columns=["Job Type", "Count", "Source"])
    for job_type in job_set:
        job_type_clean = job_type.replace('+', ' ')
        try:
            url = url_template.format(job_type, city)
            html = requests.get(url, headers=random_headers())
            sleep(3)
            soup = BeautifulSoup(html.content, 'html.parser', from_encoding="utf-8")
            total_jobs_text = soup.find('h1', {'class': "title"}).text.replace('\n', '')
            total_jobs_list = re.findall('\d+', total_jobs_text)
            if len(total_jobs_list) > 1:
                total_jobs = (int(total_jobs_list[0]) * 1000) + int(total_jobs_list[1])
            else:
                total_jobs = int(total_jobs_list[0])
        except:
            try:
                url = url_template.format(job_type, city)
                html = requests.get(url, headers=random_headers())
                sleep(3)
                soup = BeautifulSoup(html.content, 'html.parser', from_encoding="utf-8")
                total_jobs_text = soup.find('h1', {'class': "title"}).text.replace('\n', '')
                total_jobs_list = re.findall('\d+', total_jobs_text)
                if len(total_jobs_list) > 1:
                    total_jobs = (int(total_jobs_list[0]) * 1000) + int(total_jobs_list[1])
                else:
                    total_jobs = int(total_jobs_list[0])
            except:
                print ("Skipping for role of " + str(job_type_clean))
                df_more = df_more.append({'Job Type': job_type_clean, 'Count': 0, 'Source': source},
                                         ignore_index=True)
                continue
        if total_jobs == 1000:
            total_jobs = "1000+"
        print("In " + str(source) + " For : " + str(job_type_clean) + ". Total Jobs Found : " + str(total_jobs))
        df_more = df_more.append({'Job Type': job_type_clean, 'Count': total_jobs, 'Source': source}, ignore_index=True)
    return df_more

if __name__ == "__main__":
    start_time = datetime.now()
    city = "Calgary"
    out_file = "Count_" + str(city) + ".csv"
    job_set_plus = set(['software+developer', 'software+engineer', 'data+scientist', 'ux+ui+designer', 'full+stack+developer',
                          'ai+machine+learning+developer','project+manager',"electrical+engineer", "qa+engineer",
                          "cloud+developer","business+development+manager","front+end+software+developer",
                          "business+analyst","backend+developer","cyber+security+expert"])
    job_set_dash = set(['software-developer', 'software-engineer', 'data-scientist', 'ux-ui-designer', 'full-stack-developer',
                             'ai-machine-learning-developer', 'project-manager', "electrical-engineer", "qa-engineer",
                             "cloud-developer", "business-development-manager", "front-end-software-developer",
                             "business-analyst", "backend-developer", "cyber-security-expert"])
    df_indeed = get_indeed_count(job_set_plus,city)
    df_glassdoor = get_glassdoor_count(job_set_dash, city)
    df_stackoverflow = get_stackoverflow_count(job_set_plus, city)
    df_monster = get_monster_count(job_set_plus, city)
    df_all = pd.concat([df_indeed, df_glassdoor, df_stackoverflow, df_monster])
    df_all.to_csv(out_file, encoding='utf-8')
    end_time = datetime.now()
    print('Duration: {}'.format(end_time - start_time))