import csv
import requests
import time
from bs4 import BeautifulSoup
from elastic_search.utils import DuplicateHashError
from scrappers_miners.API_struct_data.xing.es_structure import Xing
from scrappers_miners.utils.utils import APIHead
from src import settings

count = 0


def create_job_role_list():
    data_file_path = settings.BASE_DIR + '/scrappers_miners/API_struct_data/xing/job_role.csv'
    data_file = open(data_file_path, 'r')
    reader = csv.reader(data_file)
    for row in reader:
        if row[0] not in (None, ""):
            if ' ' in row[0]:
                job_role = row[0].replace(' ', '+')
                yield job_role
            else:
                yield row[0]


def request_url(url):
    custom_headers = {'Accept-Language': 'en-US,en;q=0.8'}
    r = ''
    while r == '':
        try:
            r = requests.get(url, headers=custom_headers)
        except KeyboardInterrupt:
            break
        except:
            print("Connection refused by the server..")
            print("Let me sleep for 3 seconds")
            time.sleep(3)
            continue
    return r


def calculate_no_of_pages(soup):
    selector = soup.select(".search-results-summary-line span")
    if selector:
        job_count = (int(selector[0].text) / 20) + 1
        return 10 if job_count > 10 else job_count
    else:
        return 0


def yield_scrap_result(job_role, job_url):
    global count
    job_attributes = []
    r = request_url(job_url)
    soup = BeautifulSoup(r.content, 'html.parser')
    title_selector = soup.select("#job-posting-header > h1 > strong")
    company_selector = soup.select("#job-posting-header > h2 > a.b-link.job-posting-header-company")
    location_selector = soup.select("#job-posting-header > h2 > a.b-link.regular.job-posting-header-city")
    date_selector = soup.select("#job-posting-header > ul > li:nth-of-type(1) > time")
    job_type_selector = soup.select("#job-posting-header > ul > li:nth-of-type(2) > span > a")
    career_level_selector = soup.select("#job-posting-header > ul > li:nth-of-type(3)")
    industry_selector = soup.select("#job-posting-header > ul > li:nth-of-type(4) > a")
    description_selector = soup.select("#job-posting-description > div > div")
    url_selector = soup.select("#maincontent > div > div > ul > li:nth-of-type(4) > a")
    next_job_selector = soup.select('.nroute.prev-next-posting.next-posting.foundation-col-6')
    job_attributes_selectors = [title_selector, company_selector, location_selector,
                                date_selector, job_type_selector, career_level_selector,
                                industry_selector, description_selector, url_selector]

    for index, job_attributes_selector in enumerate(job_attributes_selectors):
        if index == 3:
            job_attributes.append(job_attributes_selector[0].get('datetime').encode(
                'utf-8')) if job_attributes_selector else job_attributes.append(None)
        elif index == 8:
            job_attributes.append("https://www.xing.com" + job_attributes_selector[0].get('href').encode(
                'utf-8')) if job_attributes_selector else job_attributes.append(None)
        elif index == 5:
            if job_attributes_selector:
                career_level = job_attributes_selector[0].text.strip(' \t\n\rCareer level:').encode('utf-8')
                job_attributes.append(career_level)
            else:
                job_attributes.append(None)
        else:
            job_attributes.append(
                job_attributes_selector[0].text.encode('utf-8')) if job_attributes_selector else job_attributes.append(
                None)

    count += 1
    print '%d Entries Scraped' % count

    yield Xing(
        source="Xing",
        role=job_role,
        job_title=job_attributes[0],
        organisation=job_attributes[1],
        location=job_attributes[2],
        create_time=job_attributes[3],
        job_type=job_attributes[4],
        career_level=job_attributes[5],
        industry=job_attributes[6],
        description=job_attributes[7],
        link=job_attributes[8]
    )

    if next_job_selector:
        next_job_url = "https://xing.com/jobs/" + next_job_selector[0].get('data-nroute')[14:].rstrip('"]')
        for job in yield_scrap_result(job_role, next_job_url):
            yield job


def start(job_roles, base_url):
    for index, job_role in enumerate(job_roles):
        complete_url = base_url + job_role + '&sort=date'
        r = request_url(complete_url)
        soup = BeautifulSoup(r.content, 'html.parser')
        job_selectors = soup.select(".title.job-posting-link.name-page-link")
        if job_selectors:
            first_job_url = job_selectors[0].get('href')
            try:
                for job in yield_scrap_result(job_role, first_job_url):
                    yield job
            except DuplicateHashError:
                print 'Hash Collision - Skipping %s' % job_role
                continue


class XingScrapper(APIHead):
    def execute(self):
        job_roles = create_job_role_list()
        base_url = 'https://www.xing.com/search/in/jobs?facets%5B%5D=salary&keywords='
        print("Scraping Started")
        self.data_iterator = start(job_roles, base_url)
