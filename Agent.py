from tiktok.TikTokHelper import TikTokHelper
from creator.videoNoob import VideoNoob


import numpy as np

class Agent(object):

    
    TikTok_mainStreamChannels = [  'lorengray', 'zachking', 'babyariel', 'charlidamelio', 'addisonre']
    channels = ['tiktokofficial']


    def __init__(self):
        self.tkh = TikTokHelper()
        self.vidNoob = VideoNoob()
        self.youtubeHelper = youtubeHelper()
        


    def update(self):
        '''
        Downloads recently uploaded content from main streams
        '''
        #self.dbh.update()
        for user in TikTok_mainStreamChannels:
            
            try:
                self.tkh.get_user(user, count=500)
            except:
                print('Uh oh')
                pass
        




    def findContentStreams(self, platform, tags, num_streams=10):
        '''
        Returns list of num_streams platform specific channels
        '''
        streams = []

        if platform == 'youtube':
            

            return None


        elif platform == 'tiktok':


            return None


        elif platform == 'instagram':

            return None  


    def generateContent(self, num_clips=50):
        '''
        Generates new Youtube videos based on ?? 
        '''
        '''
        # Generate content randomly 
        #TODO Modify probabilities of generating different types of content based on views 
        compilation_prob = 0.3
        user_compilation_prob = 1 - compilation_prob
        if np.random.rand() < compilation_prob:
            return self.vidNoob.generateTikTokCompilation(num_clips=num_clips)
        else:
            user = random.sample(TikTok_mainStreamChannels, 1)[0]
            return self.vidNoob.generateTikTokCompilation(user=user, num_clips=num_clips)
        '''
        return self.vidNoob.generateTikTokBattle('charlidamelio', 'lorengray')
        



    def marketContent(self, file_location):
        '''
        A function that generates a title and thumbnail based on the video data and returns
        a youtubeVideo object
        '''
        #return youtubeVideo
        return youtubeVideo

    def agentSell(self, youtubeVideo):
        pass
