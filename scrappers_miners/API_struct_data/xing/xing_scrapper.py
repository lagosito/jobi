import csv
import requests
import time
from bs4 import BeautifulSoup
from scrappers_miners.utils.utils import APIHead


class XingScrapper(APIHead):

    def execute(self):
        job_roles = create_job_role_list()
        base_url = 'https://www.xing.com/search/in/jobs?facets%5B%5D=salary&keywords='
        for job_role in job_roles:
            complete_url = base_url + job_role + '&sort=date'
            r = request_url(complete_url)
            soup = BeautifulSoup(r.content, 'html.parser')
            page_count = calculate_no_of_pages(soup)
            yield_scrap_results(soup)
            if page_count > 1:
                for page_no in range(2, page_count+1):
                    complete_url = base_url + job_role + '&page=' + str(page_no) + '&sort=date'
                    r = request_url(complete_url)
                    soup = BeautifulSoup(r.content, 'html.parser')
                    yield_scrap_results(soup)

        # FIXME: Add self.data_iterator


def create_job_role_list():
    job_role_list = []
    data_file = open('job_role.csv', 'r')
    reader = csv.reader(data_file)
    for row in reader:
        if row[0] not in (None, ""):
            if ' ' in row[0]:
                job_role = row[0].replace(' ', '+')
                job_role_list.append(job_role)
            else:
                job_role_list.append(row[0])
    return job_role_list


def request_url(url):
    r = ''
    while r == '':
        try:
            r = requests.get(url)
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


def yield_scrap_results(soup):
    job_attributes = []
    job_selectors = soup.select(".title.job-posting-link.name-page-link")
    if job_selectors:
        job_urls = [job_selector.get('href') for job_selector in job_selectors]
        print len(job_selectors), job_urls
        for job_url in job_urls:
            r = request_url(job_url)
            soup = BeautifulSoup(r.content, 'html.parser')
            title_selector = soup.select("#job-posting-header > h1 > strong")
            company_selector = soup.select("#job-posting-header > h2 > a.b-link.job-posting-header-company")
            location_selector = soup.select("#job-posting-header > h2 > a.b-link.regular.job-posting-header-city")
            time_stamp_selector = soup.select("#job-posting-header > ul > li:nth-of-type(1) > time")
            job_type_selector = soup.select("#job-posting-header > ul > li:nth-of-type(2) > span > a")
            career_level_selector = soup.select("#job-posting-header > ul > li:nth-of-type(3)")
            industry_selector = soup.select("#job-posting-header > ul > li:nth-of-type(4) > a")
            description_selector = soup.select("#job-posting-description > div > div")
            job_attributes_selector = [title_selector, company_selector, location_selector,
                                       time_stamp_selector, job_type_selector, career_level_selector,
                                       industry_selector, description_selector]
            for index, job_attributes_selector in enumerate(job_attributes_selector):
                if index != 3:
                    job_attributes.append(job_attributes_selector[0].text) if job_attributes_selector else job_attributes.append(None)
                else:
                    job_attributes.append(job_attributes_selector[0].get('datetime')) if job_attributes_selector else job_attributes.append(None)
            print job_attributes

