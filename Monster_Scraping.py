from bs4 import BeautifulSoup  # For HTML parsing
from urllib.request import urlopen  # Website connections
import re  # Regular expressions
from time import sleep  # To prevent overwhelming the server between connections
from collections import Counter  # Keep track of our term counts
import pandas as pd  # For converting results to a dataframe and bar chart plots
import unicodedata
import csv
import pandas


def text_cleaner(website):
    '''
    This function just cleans up the raw html so that I can look at it.
    Inputs: a URL to investigate
    Outputs: Cleaned text only
    '''
    text = ''
    company_name = ''
    location = ''
    industry = ''
    try:
        site = urlopen(website).read()  # Connect to the job posting
    except:
        return  # Need this in case the website isn't there anymore or some other weird connection problem

    soup_obj = BeautifulSoup(site)  # Get the html from the site

    for script in soup_obj(["script", "style"]):
        script.extract()  # Remove these two elements from the BS4 object

    try:
        site_type = "Type 1"  # During research observed that there are two different html formats across pages
        text = soup_obj.find(id="jobBodyContent").get_text()
        company_name = soup_obj.find(itemprop="name").get_text()
        location = soup_obj.find(itemprop="jobLocation").get_text()
        industry = soup_obj.find(itemprop="industry").get_text()
        experience_level = soup_obj.find(itemprop="qualifications").get_text()
    except:
        try:
            site_type = "Type 2"
            text = soup_obj.find(id="JobDescription").get_text()
            jobsummary = soup_obj.select("key")
            for tag in soup_obj.find_all("dt"):
                if tag.get_text() == "Location":
                    location = tag.find_next("dd").get_text()
                if tag.get_text() == "Job type":
                    jobtype = tag.find_next("dd").get_text()
                if tag.get_text() == "Industries":
                    industry = tag.find_next("dd").get_text()
            company = soup_obj.find(id="AboutCompany")
            for tag in company.find_all("h3"):
                company_name = tag.get_text()
        except:
            return

    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore')

    if site_type == "Type 1":
        data = [company_name, location, industry, text]
    else:
        data = [company_name, location, industry, text]
    return data


def job_info(city=None, state=None):
    final_job = 'Data-Analyst'  # searching for Data Analyst exact fit
    max_pages = 1
    # Make sure the city specified works properly if it has more than one word
    if city is not None:
        final_city = city.split()
        final_city = '+'.join(word for word in final_city)
        final_site_list = ['https://www.monster.ca/jobs/search/?q=', final_job, '&where=', final_city,
                           '__2C-', state]  # Join all of our strings together so that indeed will search correctly
    else:
        final_site_list = ['https://www.monster.ca/jobs/search/?q=', final_job,
                           '']  # if city is not provided then search for all

    final_site = ''.join(final_site_list)  # Merge the html address together into one string

    base_url = 'https://www.monster.ca/'

    print(final_site)
    try:
        #html = urlopen(final_site).read()  # Open up the front page of our search first
        response = urlopen(final_site)
        html = response.read()
    except:
        print ('That city/state combination did not have any jobs. Exiting . . .')  # In case the city is invalid
        return
    soup = BeautifulSoup(html, "html.parser")
    # Now find out how many jobs there were
    num_jobs_area = soup.find(class_='page-title visible-xs')
    num_jobs = num_jobs_area.get_text()
    job_numbers = re.findall('\d+', num_jobs)
    total_num_jobs = int(job_numbers[0])
    num_pages = total_num_jobs / 24
    city_title = city
    num_pages = int(num_pages)
    print(type(num_pages))
    if city is None:
        city_title = 'Nationwide'
    print('There were', total_num_jobs, 'jobs found in ', city_title)  # Display how many jobs were found
    job_descriptions = []
    for i in range(1, num_pages + 1):  # Loop through all of our search result pages
        print('Getting page', i)
        start_num = str(i * 10)  # Assign the multiplier of 10 to view the pages we want
        current_page = ''.join([final_site, '&page=', str(i)])
        print("Current Page : ", current_page)
        # Now that we can view the correct 10 job returns, start collecting the text samples from each
        response_page = urlopen(current_page)
        html_page = response_page.read()  # Get the page
        print (html_page)
        page_obj = BeautifulSoup(html_page, "html.parser")  # Locate all of the job links
        job_link_area = page_obj.find(id="resultsWrapper")  # The center column on the page where the job postings exist
        print("Job Link Area " + job_link_area)
        try:
            job_URLS = [link.get('href') for link in job_link_area.find_all('a')]
            print ("Job URLS" + ob_URLS)
            job_URLS = filter(lambda x: 'https://job-openings' in x, job_URLS)  # Now get just the job related URLS
            print('Jobs Found : ', len(job_URLS))
            for j in range(0, len(job_URLS)):
                final_description = text_cleaner(job_URLS[j])
                if final_description:  # So that we only append when the website was accessed correctly
                    job_descriptions.append(final_description)
                    print("Jobs Written so Far from this page : ", len(job_descriptions))
                sleep(
                    5)  # So that we don't be jerks. If you have a very fast internet connection you could hit the server a lot!
        except:
            print("Error Occurred!")

    return job_descriptions
    print('Done with collecting the job postings!')
    print('There were', len(job_descriptions), 'jobs successfully found.')
    csvfile = "C:/Users/a.vivek/Desktop/Projects/Calgary/Monster.csv"
    with open(csvfile, "a") as output:
        writer = csv.writer(output, lineterminator='\n')
        writer.writerows(job_descriptions)

Job_Postings = job_info() # Another way to call this function would be job_info('Toronto','ON')
