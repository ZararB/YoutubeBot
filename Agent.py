from DbHelper import DbHelper
from TikTokHelper import TikTokHelper
from videoNoob import VideoNoob
import random 
class Agent(object):

    global TikTok_mainStreamChannels
    TikTok_mainStreamChannels = ['charlidamelio', 'lorengray', 'zachking', 'addisonre', 'babyariel']
    channels = ['tiktokofficial']


    def __init__(self):
        self.dbh = DbHelper('data/databases/memes.db')
        self.tkh = TikTokHelper()
        self.vidNoob = VideoNoob()
        pass


    def update(self):
        '''
        Downloads recently uploaded content from main streams
        '''
        for user in TikTok_mainStreamChannels:
            self.tkh.get_user(user, count=10)




    


    def generateContent(self):
        '''
        Generates new Youtube videos based on ?? 
        '''

        randomUser = random.sample(TikTok_mainStreamChannels, 1)
        file_location, title, desc = self.vidNoob.generateTikTokVideo(randomUser, 'userCompilation')

        return file_location, title, desc



