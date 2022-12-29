from bs4 import BeautifulSoup
from lxml import etree
import requests
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from datetime import datetime
import os

CHROME_DRIVER_PATH = os.getcwd() + '/chromedriver'


HEADERS = ({'User-Agent':
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 \
            (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
            'Accept-Language': 'en-US, en;q=0.5'})

STARS_XPATH = '//*[@id="repo-stars-counter-star"]'
FORKS_XPATH = '//*[@id="repo-network-counter"]'
WATCH_XPATH = '//*[@id="repo-content-pjax-container"]/div/div/div[3]/div[2]/div/div[1]/div/div[6]/a/strong'

COMMITS_XPATH = '//*[@id="repo-content-pjax-container"]/div/div/div[3]/div[1]\
    /div[2]/div[1]/div/div[4]/ul/li/a/span/strong'

TITLE_XPATH = '//*[@id="repository-container-header"]/div[1]/\
    div/div/strong/a'


class Project:
    def __init__(self, id, title, url, num_stars, num_forks, num_watches,
                 num_contributors, num_releases, num_users, num_commits, time_stamp):
        self.id = id
        self.title = title
        self.url = url
        self.num_stars = num_stars
        self.num_forks = num_forks
        self.num_watches = num_watches
        self.num_contributors = num_contributors
        self.num_releases = num_releases
        self.num_users = num_users
        self.num_commits = num_commits
        self.time_stamp = time_stamp

    def __str__(self):
        return self.id + ", " + self.title + ", " + self.url + ", " + str(self.num_stars) + ", " + \
            str(self.num_forks) + ", " + str(self.num_watches) + ", " + \
            str(self.num_contributors) + ", " + str(self.num_releases) + ", " + \
            str(self.num_users) + ", " + str(self.num_commits) + \
            ", " + str(self.time_stamp)

    def return_obj(self):
        # Return the object so you could write into
        return (self.id, self.title, self.url,
                self.num_stars, self.num_forks, self.num_watches,
                self.num_contributors, self.num_releases, self.num_users,
                self.num_commits, self.time_stamp)


def convert_to_number(raw_text):
    # Converts the raw text into a readable number
    raw_text = raw_text.replace(",", "")
    if raw_text[-1] == 'k':
        return int(float(raw_text[:-1]) * 1000)
    else:
        return int(raw_text)


def get_stars(dom):
    # Finds how many times the project was starred
    raw_text = dom.xpath(STARS_XPATH)[0].text
    return convert_to_number(raw_text)


def get_watches(soup):
    # Finds how many people are watching the project
    element = soup.find_all("div", class_="mt-2")[-2]
    strong_element = element.find("strong")
    raw_text = strong_element.text
    return convert_to_number(raw_text)


def get_forks(dom):
    # Finds how many times the project was forked
    raw_text = dom.xpath(FORKS_XPATH)[0].text
    return convert_to_number(raw_text)


def get_other_data(soup):
    # Returns the cleaned data for contributors, releases, and users
    elements = soup.find_all("div", class_="BorderGrid-row")
    raw_users, raw_contributors, raw_releases = None, None, None
    for element in elements:
        header = element.find("h2", class_="h4 mb-3")
        if header is None:
            continue
        else:
            # Find the title
            try:
                title_raw = header.find("a").text.strip("\n")
                lst = title_raw.split()
                if len(lst) == 3:
                    # That must be the user number
                    raw_users = lst[-1]
                else:
                    if lst[0] == "Releases" and len(lst) == 2:
                        # This is the releases
                        raw_releases = lst[-1]
                    elif lst[0] == "Contributors" and len(lst) == 2:
                        # This is the contributors
                        raw_contributors = lst[-1]
            except:
                continue

    # TODO: Make a function out of this repetitive code
    if raw_contributors is not None:
        contributors = convert_to_number(raw_contributors)
    else:
        contributors = None

    if raw_releases is not None:
        releases = convert_to_number(raw_releases)
    else:
        releases = None

    if raw_users is not None:
        users = convert_to_number(raw_users)
    else:
        users = None

    return contributors, releases, users


def get_links(PATH="data/project_links.txt"):
    # Read the file
    f = open(PATH, "r")
    return f.readlines()


def get_commits(dom):
    # Finds how many times the project was committed
    try:
        raw_text = dom.xpath(COMMITS_XPATH)[0].text
        return convert_to_number(raw_text)
    except:
        return None


def get_title(dom):
    # Finds the title of a given project
    raw_text = dom.xpath(TITLE_XPATH)[0].text
    return raw_text


def generate_id(url):
    # Returns a unique ID
    return str(hash(url))[1:13]


def scrape_page(url, dt):
    # Scrapes a given Github url for the desired statistics
    webpage = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(webpage.content, "html.parser")
    dom = etree.HTML(str(soup))

    # Get all the information about the project
    stars = get_stars(dom)
    forks = get_forks(dom)
    watches = get_watches(soup)
    commits = get_commits(dom)
    title = get_title(dom)

    contributors, releases, users = get_other_data(soup)

    id = generate_id(url)

    project = Project(id, title, url, stars, forks,
                      watches, contributors, releases, users, commits, dt)
    return project


def main():
    dt = int(datetime.now().timestamp())
    links = [link.strip("\n") for link in get_links()]
    for link in links:
        scrape_page(link, dt)
