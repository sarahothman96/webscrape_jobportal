import requests
from bs4 import BeautifulSoup
from requests.models import LocationParseError

url = 'https://malaysia.indeed.com/jobs?q=Data+Engineer&l=Malaysia'
page = requests.get(url)
soup = BeautifulSoup(page.content, 'html.parser')

results = soup.find(id='resultsBodyContent')
#print(results.prettify())

job_elems = results.find_all('div', class_='jobsearch-SerpJobCard')

for job_elem in job_elems:
    title_elem = job_elem.find('h2', class_='title')
    company_elem = job_elem.find('span', class_='company')
    location_elem = job_elem.find('span', class_='location accessible-contrast-color-location')
    date_elem = job_elem.find('span', class_='date date-a11y')
    if None in (title_elem, company_elem, location_elem, date_elem):
        continue
    print(title_elem.text.strip())
    print(company_elem.text.strip())
    print(location_elem.text.strip())
    print(date_elem.text.strip())
    print()
