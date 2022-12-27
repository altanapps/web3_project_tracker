import time
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException

CHROME_DRIVER_PATH = '/Users/altantutar/Desktop/chromedriver'
HOMEPAGE = "https://github.com/topics/blockchain"
LOAD_MORE = "/html/body/div[1]/div[4]/main/div[2]/div[2]/div/div[1]/form/button"
ARTICLES = "/html/body/div[1]/div[5]/main/div[2]/div[2]/div/div[1]/article[1]"
NUM_ARTICLES = 20
SLEEP_SECONDS = 1


def write(project_links):
    # Write the results to a text file for now
    with open('data/project_links.txt', 'w') as f:
        for file in project_links:
            f.write(file + "\n")


def save_results(driver):
    # You should have loaded all the items now,
    # download all the links
    project_links = driver.find_elements_by_xpath(
        './/article/div/div/div/h3/a[2]')
    project_links = [link.get_attribute('href') for link in project_links]
    print(len(project_links))

    # Write all these projects into a text file
    write(project_links)


def find_all_projects():
    #############################
    # LOADS ONLY 1,000 Projects #
    #############################

    # Set up the browser options
    browser_options = ChromeOptions()
    # browser_options.headless = True
    driver = Chrome(executable_path=CHROME_DRIVER_PATH,
                    options=browser_options)
    driver.get(HOMEPAGE)
    
    loaded = NUM_ARTICLES
    while True:
        try:
            # Find the button and click it to get more data
            driver.find_element_by_xpath(LOAD_MORE).click()
            time.sleep(SLEEP_SECONDS)
            loaded += NUM_ARTICLES
        except NoSuchElementException:
            save_results(driver)
            break
        except:
            continue

    save_results(driver)


find_all_projects()
