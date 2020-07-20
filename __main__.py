
from Agent import Agent
from youtubeHelper import youtubeHelper

if __name__ == '__main__':

    ytHelper = youtubeHelper()
    agent = Agent()
    #agent.update()
    file_location, title, desc = agent.generateContent()
    
    ytHelper.upload_video('tiktokofficial', file_location, title, desc)

