import requests
from selenium import webdriver
import time
import logging
import pandas as pd

#Set log
logging.basicConfig(filename='abcnet.log', level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


def get_next(driver):
    x = driver.find_elements_by_class_name('pagination-nav__next')
    return x

def get_url_list(driver, topic_page, url_list):
    # Get Page
    driver.get(topic_page)
    time.sleep(20)
    print('Get Page Success')
    logging.info('Get Page Success')

    x = driver.find_element_by_class_name('article-index')
    y = x.find_elements_by_tag_name('h3')
    #print(y)
    for i in y:
        z = i.find_element_by_tag_name('a')
        url_list.append(z.get_attribute('href'))
        
    #return url_list

def get_data(driver, url):
    # Get Page
    driver.get(url)
    time.sleep(30)
    x = driver.find_element_by_id('body')
    y = x.find_elements_by_tag_name('p')
    output = ''
    for i in y:
        output += i.text
    print(f'Get Page {url} Success')
    logging.info(f'Get Page {url} Success')
    return output

def process_url_list(url_list):
    chrome_options = webdriver.ChromeOptions()
    # set chrome start option headless and disable gpu
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(options=chrome_options)
    data_list = []
    count = 0
    for url in url_list:
        count += 1
        #Restart webdriver every 8 news
        if count >= 8:
            count = 0
            driver.quit()
            time.sleep(30)
            driver = webdriver.Chrome(options=chrome_options)
        try:
            data = get_data(driver, url)
        except Exception as e:
            print(f'Get Data {url} Error')
            logging.info(f'Exception on Page {url}: {e}')
        data_list.append(data)
    driver.quit()
    return data_list

chrome_options = webdriver.ChromeOptions()
# set chrome start option headless and disable gpu
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
#chrome_options.add_argument('log-level=3')
driver = webdriver.Chrome(options=chrome_options)

url_list = []
#topic_page = 'https://hollywoodlife.com/topics/news/'

topic_pages = [
    'https://www.abc.net.au/news/sport/athletics/',
    'https://www.abc.net.au/news/sport/basketball/',
    'https://www.abc.net.au/news/sport/cycling/',
    'https://www.abc.net.au/news/sport/golf/',
    'https://www.abc.net.au/news/sport/horseracing/',
    'https://www.abc.net.au/news/sport/tennis/',
    'https://www.abc.net.au/news/sport/swimming/',
    'https://www.abc.net.au/news/business/articles/',
    'https://www.abc.net.au/news/business/articles/?page=3',
    'https://www.abc.net.au/news/business/articles/?page=5',
    'https://www.abc.net.au/news/business/articles/?page=7'
    ,'https://www.abc.net.au/news/business/articles/?page=9'
]

for topic_page in topic_pages:
    get_url_list(driver, topic_page, url_list)
driver.quit()
logging.info('Get URL Success')
print('Get URL Success')

with open('urls_abcnet.txt', 'w') as of:
    for url in url_list:
        of.write(url)
        of.write('\n')

data_list = process_url_list(url_list)
logging.info('Get ALL NEWS Success')
print('Get ALL NEWS Success')

data_list = pd.DataFrame(data_list)
data_list.rename(columns={0:'text'},inplace=True)
label = [0 for i in range(data_list.shape[0])]
data_list['label'] = label
data_list.to_json('abcnet.json')

