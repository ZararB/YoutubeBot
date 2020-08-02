from Agent import Agent
from youtubeHelper import youtubeHelper
import subprocess


ytHelper = youtubeHelper()
agent = Agent()


try:
    agent.update()
    pass
except:
    pass

#file_location, title, desc = agent.generateContent()
#youtubeVid = agent.marketContent(file_location)
#agent.reflect()


ytHelper.upload_video('tiktokofficial', file_location, title, desc)
with open('log.txt', 'a') as logFile:
    logFile.write('Uploaded Youtube video' + file_location + title + desc)


