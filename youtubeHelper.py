from selenium import webdriver 
from selenium.webdriver.common.keys import Keys
import time
import subprocess

class youtubeHelper():


    def __init__(self):

        pass


    def login(self, username, password):
        self.driver.get("https://accounts.google.com/signin/v2/identifier?service=youtube&uilel=3&passive=true&continue=https%3A%2F%2Fwww.youtube.com%2Fsignin%3Faction_handle_signin%3Dtrue%26app%3Ddesktop%26hl%3Den%26next%3Dhttps%253A%252F%252Fwww.youtube.com%252F&hl=en&ec=65620&flowName=GlifWebSignIn&flowEntry=ServiceLogin")
        emailElement = self.driver.find_element_by_name("identifier")
        emailElement.send_keys(username + Keys.RETURN)
        time.sleep(3)
        passwordElement = self.driver.find_element_by_name("password")
        passwordElement.send_keys(password + Keys.RETURN)

        self.loggedIn = True 
        pass 

    def upload_video(self, filepath, title, description):


        subprocess.run(["python3", "upload_video.py", 
        "--file="+filepath, "--title="+title, "--description="+description])

        
