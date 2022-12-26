from bs4 import BeautifulSoup
from lxml import etree
import requests

HEADERS = ({'User-Agent':
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 \
            (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
            'Accept-Language': 'en-US, en;q=0.5'})

STARS_XPATH = '//*[@id="repo-stars-counter-star"]'
FORKS_XPATH = '//*[@id="repo-network-counter"]'
WATCH_XPATH = '//*[@id="repo-content-pjax-container"]/div/div/div[3]/div[2]/div/div[1]/div/div[6]/a/strong'


# RELEASES_XPATH = '//*[@id="repo-content-pjax-container"]/div/div/div[3]\
#   /div[2]/div/div[2]/div/h2/a/span'
# CONTRIBUTORS_XPATH = '//*[@id="repo-content-pjax-container"]/div/div/\
#   div[3]/div[2]/div/div[4]/div/h2/a/span'
# USERS_XPATH = '//*[@id="repo-content-pjax-container"]/div/div/\
#   div[3]/div[2]/div/div[3]/div/h2/a/span'
# COMMITS_XPATH = '//*[@id="repo-content-pjax-container"]/div/div/div[3]/div[1]/\
#     div[2]/div[1]/div/div[4]/ul/li/a/span/strong'
# TITLE_XPATH = '//*[@id="readme"]/div[2]/article/h1'


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


# def get_number_releases(dom):
#     # Finds how many times the project had releases
#     raw_text = dom.xpath(RELEASES_XPATH)[0].text
#     return convert_to_number(raw_text)


# def get_number_contributors(dom):
#     # Finds how many contributors does the project have
#     raw_text = dom.xpath(CONTRIBUTORS_XPATH)[0].text
#     return convert_to_number(raw_text)


# def get_number_used_by(dom):
#     # Finds how many people are using the project
#     raw_text = dom.xpath(USERS_XPATH)[0].text
#     return convert_to_number(raw_text)


# def get_number_commits(dom):
#     # Finds how many times code was committed to the project
#     raw_text = dom.xpath(COMMITS_XPATH)[0].text
#     return convert_to_number(raw_text)


def get_links(PATH="data/project_links.txt"):
    # Read the file
    f = open(PATH, "r")
    return f.readlines()


def scrape_page(url):
    # Scrapes a given Github url for the desired statistics
    webpage = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(webpage.content, "html.parser")
    dom = etree.HTML(str(soup))

    # Get all the information about the project
    stars = get_stars(dom)
    forks = get_forks(dom)
    watches = get_watches(soup)

    # releases = get_number_releases(dom)
    # contributors = get_number_contributors(dom)
    # users = get_number_used_by(dom)
    # commits = get_number_commits(dom)

    return(stars, forks, watches)


def main():
    links = [link.strip("\n") for link in get_links()]
    for link in links:
        print(link)
        print(scrape_page(link))


main()
