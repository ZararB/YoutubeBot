from selenium import webdriver 
from selenium.webdriver.common.keys import Keys
import time


class YoutubeAPI():


    def __init__(self):

        self.driver = webdriver.Firefox()
        self.loggedIn = False
        #self.driver.get("https://www.youtube.com")


    def login(self, username, password):
        self.driver.get("https://accounts.google.com/signin/v2/identifier?service=youtube&uilel=3&passive=true&continue=https%3A%2F%2Fwww.youtube.com%2Fsignin%3Faction_handle_signin%3Dtrue%26app%3Ddesktop%26hl%3Den%26next%3Dhttps%253A%252F%252Fwww.youtube.com%252F&hl=en&ec=65620&flowName=GlifWebSignIn&flowEntry=ServiceLogin")
        emailElement = self.driver.find_element_by_name("identifier")
        emailElement.send_keys(username + Keys.RETURN)
        time.sleep(3)
        passwordElement = self.driver.find_element_by_name("password")
        passwordElement.send_keys(password + Keys.RETURN)

        self.loggedIn = True 
        pass 

    def upload_video(self, video):

        if self.loggedIn == False:
            print("No user logged in")
            return None

        self.driver.get("https://studio.youtube.com/channel/UCCHt350Wl-3a13Ugz-3aXWQ/videos/upload?d=ud&filter=%5B%5D&sort=%7B%22columnType%22%3A%22date%22%2C%22sortOrder%22%3A%22DESCENDING%22%7D")

        fileInput = self.driver.find_element_by_id("select-files-button")
        #fileInput.click()
        fileInput.send_keys("/home/zarar/YoutubeBot/data/videos/firstvid.mp4")


        





yta = YoutubeAPI()
yta.login("quickdophit@gmail.com", "Tranzitround32!")
time.sleep(5)
yta.upload_video("hello")    
