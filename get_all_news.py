import requests
from selenium import webdriver
import time
import logging
import pandas as pd

#Set log
logging.basicConfig(filename='logger.log', level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


def get_next(driver):
    x = driver.find_element_by_class_name('text-center')
    y = x.find_elements_by_class_name('next')
    return y

def get_url_list(driver, topic_page, url_list):
    # Get Page
    driver.get(topic_page)
    time.sleep(20)
    print('Get Page Success')
    logging.info('Get Page Success')
    
    x = driver.find_element_by_xpath('/html/body/div[4]/div[2]/section/section/div/div[1]')
    y = x.find_elements_by_class_name('story-title')
    #print(y)
    for i in y:
        z = i.find_element_by_tag_name('a')
        url_list.append(z.get_attribute('href'))
    
    next_page = get_next(driver)
    if next_page:
        time.sleep(10)
        a = next_page[0].find_element_by_tag_name('a').get_attribute('href')
        get_url_list(driver, a, url_list)
        

    #return url_list
def get_data(driver, url):
    # Get Page
    driver.get(url)
    time.sleep(30)
    x = driver.find_element_by_xpath('/html/body/div[4]/div[2]/section/section[1]/div/div/div[4]')
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

url_list = []
chrome_options = webdriver.ChromeOptions()
# set chrome start option headless and disable gpu
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
driver = webdriver.Chrome(options=chrome_options)

#topic_page = 'https://news.un.org/en/news/topic/climate-change'
'''
topic_pages = ['https://news.un.org/en/news/topic/law-and-crime-prevention/date/2020',
                'https://news.un.org/en/news/topic/law-and-crime-prevention/date/2019',
                'https://news.un.org/en/news/topic/law-and-crime-prevention/date/2018']
'''
topic_pages = ['https://news.un.org/en/news/topic/economic-development/date/2020',
                'https://news.un.org/en/news/topic/economic-development/date/2019',
                'https://news.un.org/en/news/topic/economic-development/date/2018']

for topic_page in topic_pages:
    get_url_list(driver, topic_page, url_list)
driver.quit()
logging.info('Get URL Success')
print('Get URL Success')

with open('urls.txt', 'w') as of:
    for url in url_list:
        of.write(url)
        of.write('\n')

'''
with open('urls.txt', 'r') as of:
    url_list = [line.strip() for line in of.readlines()]
'''

data_list = process_url_list(url_list)
logging.info('Get ALL NEWS Success')
print('Get ALL NEWS Success')

data_list = pd.DataFrame(data_list)
data_list.rename(columns={0:'text'},inplace=True)
label = [0 for i in range(data_list.shape[0])]
data_list['label'] = label
data_list.to_json('un_news_economic-development.json')

