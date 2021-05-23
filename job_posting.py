import urllib
import requests
from bs4 import BeautifulSoup
import pandas as pd
import os


def find_jobs_from(website, job_title, location, specific_characs, filename="big_dataengineer_result.xlsx"):
    """
    This function extracts all the specific characteristics of all new job postings
    of the title and location specified and returns them in single file.
    The arguments it takes are:
        - Website: Indeed
        - Job_title
        - Location
        - Specific_characs: this is a list of the job characteristics of interest,
            from title, companies, links and date_listed.
        - Filename: to specify the filename and format of the output.
            Deafault is .xlsx file called 'data_science_results.xlsx'

    """
    
    if website == 'Indeed':
        job_soup = load_indeed_jobs_div(job_title, location)
        jobs_list, num_listings = extract_job_information_indeed(job_soup, specific_characs)
        
        save_jobs_to_excel(jobs_list, filename)
        print('{} new job postings retrieved from {}. Stored in {}.'.format(num_listings, website, filename))

def save_jobs_to_excel(jobs_list, filename):
    jobs = pd.DataFrame(jobs_list)
    jobs.to_excel(filename)

def load_indeed_jobs_div(job_title, location):
    getVars = {'q':job_title, 'l':location, 'fromage':'last', 'sort':'date'}
    url = ('https://malaysia.indeed.com/jobs?' + urllib.parse.urlencode(getVars))
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    job_soup = soup.find(id="resultsCol")
    return job_soup

def extract_job_information_indeed(job_soup, specific_characs):
    job_elems = job_soup.find_all('div', class_="jobsearch-SerpJobCard")

    cols = []
    extracted_info = []

    if 'titles' in specific_characs:
        titles = []
        cols.append('titles')
        for job_elem in job_elems:
            titles.append(extract_job_title_indeed(job_elem))
        extracted_info.append(titles)

    if 'companies' in specific_characs:
        companies = []
        cols.append('companies')
        for job_elem in job_elems:
            companies.append(extract_company_indeed(job_elem))
        extracted_info.append(companies)

    if 'links' in specific_characs:
        links = []
        cols.append('links')
        for job_elem in job_elems:
            links.append(extract_link_indeed(job_elem))
        extracted_info.append(links)

    if 'date_listed' in specific_characs:
        dates = []
        cols.append('date_listed')
        for job_elem in job_elems:
            dates.append(extract_date_indeed(job_elem))
        extracted_info.append(dates)

    jobs_list = {}

    for j in range(len(cols)):
        jobs_list[cols[j]] = extracted_info[j]

    num_listings = len(extracted_info[0])

    return jobs_list, num_listings

def extract_job_title_indeed(job_elem):
    title_elem = job_elem.find('h2', class_='title')
    title = title_elem.text.strip()
    return title

def extract_company_indeed(job_elem):
    company_elem = job_elem.find('span', class_='company')
    company = company_elem.text.strip()
    return company

def extract_link_indeed(job_elem):
    link = job_elem.find('a')['href']
    link = 'https://malaysia.indeed.com/' + link
    return link

def extract_date_indeed(job_elem):
    date_elem = job_elem.find('span', class_='date')
    date = date_elem.text.strip()
    return date

specific_characs = ['titles', 'companies', 'links', 'date_listed']

find_jobs_from('Indeed', 'big data engineer', 'malaysia', specific_characs)
print(find_jobs_from)