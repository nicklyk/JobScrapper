'''
A program that looks for specific Job Offerings on Stackoverflow, and writes them to a csv.
IMPORTANT: Sometimes the script raises a "StaleElementReferenceException". This happens when
the script tries to grab an object which hasn't fully loaded yet.

This tool is for personal use. Don't use it to spam Stackoverflow.
'''

import csv
import argparse
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import StaleElementReferenceException

options = Options()
options.add_argument("-headless")
parser = argparse.ArgumentParser()
parser.add_argument("-kw", "--keyword", help="(str) Term to search for (default:'Programming')")
parser.add_argument("-p", "--pages", help="(int) Number of pages. 1 page = 25 Job Offerings (default: 1)", type=int)
args = parser.parse_args()

term = args.keyword if args.keyword else 'Programming'
n_pages = args.pages if args.pages else 1

fox = webdriver.Firefox()
fox.get(f'https://stackoverflow.com/jobs?q={term}')


# FIXME: Fix wait_to_load, should wait until element in DOM and not stale
def wait_to_load(browser, elem):
    wait = WebDriverWait(browser, 5, ignored_exceptions=StaleElementReferenceException)
    return wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, f'{elem}')))


def job_analysis(browser):
    """
    A function to grab all the details of the job offering on display.
    """
    wait_to_load(browser, 'section.mb32')
    about = browser.find_element_by_css_selector('section.mb32').text
    wait_to_load(browser, 'a.fc-black-900')
    job_title = browser.find_element_by_css_selector('a.fc-black-900').text
    link = browser.find_element_by_css_selector('a.fc-black-900').get_attribute('href').rsplit('?')[0]
    while True:
        temp = {}
        temp.update({'Title': job_title})
        temp.update({'Link': link})
        for line in about.splitlines():  # Iterate over the lines of 'about'
            try:
                key = line.rsplit(': ')[0]  # Split the line at ': ' and take everything left of it
                value = line.rsplit(': ')[1]  # Split the line at ': ' and take everything right of it
                temp.update({key: value})
            except:
                continue
        break

    return temp


# TODO: Apply fix for multiple pages option. ATM works for only 1 page
def all_jobs(browser, pages):
    """
    Runs through the list of job offerings on the website, extracting all the details
    using job_analysis()
    """
    wait = WebDriverWait(browser, 5)
    job_desc = []
    link_selector = 'h2.mb4.fc-black-800.fs-body3'
    browser.find_element_by_css_selector('a.s-btn__muted').click()  # Accept Privacy Policy, cookies ...
    for page in range(pages):
        n_elements = len(browser.find_elements_by_css_selector(f'{link_selector}'))  # Number of job offerings
        length_list = [x for x in range(n_elements + 1)]
        for num in length_list[1:]:
            to_click = browser.find_elements_by_css_selector(f'{link_selector}')  # Find the objects to click on
            job_desc.append(job_analysis(browser))  # Analyze the job offering
            if num < length_list[-1]:
                to_click[num].click()  # Click on the next job offering
        if len(browser.find_elements_by_class_name('s-pagination')) > 0:  # Check to see if there are multiple pages
            browser.find_elements_by_class_name('s-pagination')[-1].click()  # Load the next page
            wait.until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'body.unified-theme')))
        else:
            return job_desc
    return job_desc


def csv_create(li):
    with open(f'{term}_jobs.csv', mode='w') as file:
        fieldnames = ['Title', 'Job type', 'Experience level', 'Role', 'Industry', 'Company size', 'Company type',
                      'Link']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(li)


if __name__ == '__main__':
    jobs_list = all_jobs(fox, n_pages)
    csv_create(jobs_list)
    fox.close()
