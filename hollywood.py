import requests
from selenium import webdriver
import time
import logging
import pandas as pd

#Set log
logging.basicConfig(filename='hollywood.log', level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


def get_next(driver):
    x = driver.find_elements_by_class_name('pagination-nav__next')
    return x

def get_url_list(driver, topic_page, url_list):
    # Get Page
    driver.get(topic_page)
    time.sleep(20)
    print('Get Page Success')
    logging.info('Get Page Success')

    x = driver.find_element_by_xpath('/html/body/div[2]/main')
    y = x.find_elements_by_class_name('article-feed__article-figure')
    #print(y)
    for i in y:
        z = i.find_element_by_tag_name('a')
        url_list.append(z.get_attribute('href'))
        
    #return url_list

def get_data(driver, url):
    # Get Page
    driver.get(url)
    time.sleep(30)
    x = driver.find_element_by_class_name('rich-text.article-body--article')
    print(f'Get Page {url} Success')
    logging.info(f'Get Page {url} Success')
    return x.text

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
driver = webdriver.Chrome(options=chrome_options)

url_list = []
#topic_page = 'https://hollywoodlife.com/topics/news/'

topic_pages = [f'https://hollywoodlife.com/topics/news/page/{i}/' for i in range(1,600,50)]

for topic_page in topic_pages:
    get_url_list(driver, topic_page, url_list)
driver.quit()
logging.info('Get URL Success')
print('Get URL Success')

with open('urls.txt', 'w') as of:
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
data_list.to_json('hollywood.json')

