from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
import time 
import datetime 

def experiment1_selenium(channels, T=2.0):
    '''
    Given a list of N youtube channels, request their video page and sleep for T seconds 
    (scraping the data will require some time and we should also sleep for some time to 
    reduce chance of being flagged/prompted)
    
    '''

    t0 = time.time()
    N = len(channels)
    
    fireFoxOptions = webdriver.FirefoxOptions()
    fireFoxOptions.set_headless()
    driver = webdriver.Firefox(firefox_options=fireFoxOptions)



    for n, channel in enumerate(channels):

        
        channel_vids_url = channel + '/videos'

        driver.get(channel)

        try:
            captcha = driver.find_element(By.ID, 'rc-anchor-container')
            print('Captcha prompted afer {} requests'.format(n))
            return n

        except NoSuchElementException as e:
            wait = WebDriverWait(driver, T)
            continue 

    tf = time.time()
    time_taken = str(datetime.timedelta(seconds=tf-t0))
    print('Experiment duration: {}'.format(time_taken))
    print('Went through entire list of channels with no prompts. Increase N.')
    

