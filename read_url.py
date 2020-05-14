import requests
from selenium import webdriver
import time
import logging
import pandas

#Set log
logging.basicConfig(filename='logger.log', level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


def get_next(driver):
    x = driver.find_element_by_class_name('text-center')
    y = x.find_elements_by_class_name('next')
    return y

def get_url_list(driver, topic_page, url_list):
    # Get Page
    driver.get(topic_page)
    time.sleep(5)
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
    time.sleep(5)
    print('Get Page Success')
    logging.info('Get Page Success')
    
    x = driver.find_element_by_xpath('/html/body/div[4]/div[2]/section/section[1]/div/div/div[4]')
    return x.text

def process_url_list(url_list):
    chrome_options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(options=chrome_options)
    data_list = []
    for url in url_list:
        data = get_data(driver, url)
        data_list.append(data)
    driver.quit()
    return data_list






