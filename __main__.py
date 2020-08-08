from Agent import Agent
from youtubeHelper import youtubeHelper
import subprocess
from exceptions import *

ytHelper = youtubeHelper()
agent = Agent()


try:
    agent.update()
    pass
except:
    pass


while True:
    try:
        file_location, title, desc = agent.generateContent()
        break
    except:
        pass

    
#youtubeVid = agent.marketContent(file_location)
#agent.reflect()


ytHelper.upload_video('tiktokofficial', file_location, title, desc)
with open('log.txt', 'a') as logFile:
    logFile.write('Uploaded Youtube video' + file_location + title + desc)
