from selenium import webdriver 
from selenium.webdriver.common.keys import Keys



driver = webdriver.Firefox()
driver.get("https://www.youtube.com")
search_bar = driver.find_element_by_name("search_query")
search_bar.send_keys("Joe Rogan" + Keys.RETURN)



class YoutubeAPI():


    def __init__(self):

        self.driver = webdriver.Firefox()
        self.driver.get("https://www.youtube.com")


    def login(self, username, password):

        pass 

    def upload_video(self, video):
        pass

    
