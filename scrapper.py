from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from selenium.common.exceptions import StaleElementReferenceException
import csv
import argparse
from time import sleep

options = Options()
options.headless = True
parser = argparse.ArgumentParser()
parser.add_argument("-k", "--keyword", help="(str) Term to search for (default:'Programming')", type=str)
parser.add_argument("-p", "--pages", help="(int) Number of pages. 1 page = 25 Job Offerings (default: 1)", type=int)
args = parser.parse_args()
keyword = args.keyword if args.keyword else 'Programming'
pages = args.pages if args.pages else 1


def init_browser(term):
    browser = webdriver.Firefox()
    browser.get(f'https://stackoverflow.com/jobs?q={term}')
    cookies = browser.find_element(By.CSS_SELECTOR, 'button.js-accept-cookies')
    cookies.click()
    return browser


def wait_to_load(browser, selector):
    ignored_exceptions = (StaleElementReferenceException, )
    return WebDriverWait(browser, 5, ignored_exceptions=ignored_exceptions) \
        .until(ec.presence_of_element_located((By.CSS_SELECTOR, selector)))


def single_job(browser):
    about = wait_to_load(browser, 'section.mb32')
    job_title = wait_to_load(browser, 'a.fc-black-900').text
    link = wait_to_load(browser, 'a.fc-black-900').get_attribute('href').rsplit('?')[0]

    while True:
        temp = {}
        temp.update({'Title': job_title})
        temp.update({'Link': link})
        for line in about.text.splitlines():
            try:
                key = line.rsplit(': ')[0]
                value = line.rsplit(': ')[1]
                temp.update({key: value})
            except:
                continue
        break
    return temp


def single_page(browser):
    single_job_header = 'h2.mb4.fc-black-800.fs-body3'
    all_jobs = browser.find_elements(By.CSS_SELECTOR, f'{single_job_header}')
    jobs = []
    for x in range(1, len(all_jobs) + 1):
        jobs.append(single_job(browser))
        if x < len(all_jobs):
            all_jobs[x].click()
            sleep(0.5)
    return jobs


# TODO: Apply fix for multiple pages option. ATM works for only 1 page
def collect_jobs(browser, pages_to_query):
    jobs = []
    for page in range(pages_to_query):
        jobs.extend(single_page(browser))
    return jobs


def csv_create(li):
    with open(f'{keyword}_jobs.csv', mode='w') as file:
        fieldnames = ['Title', 'Job type', 'Experience level', 'Role', 'Industry', 'Company size', 'Company type',
                      'Link']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(li)


if __name__ == '__main__':
    fox = init_browser(keyword)
    jobs_list = collect_jobs(fox, pages)
    csv_create(jobs_list)
    fox.quit()
