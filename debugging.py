from youtube.youtube_api.scraper_api import search_youtube
from youtube.youtube_api.scraper_api import scrape_channels
from database.youtube import get_unscraped_channel_urls

from tiktok import TikTokHelper
from creator.videoNoob import VideoNoob
if __name__ == '__main__':
    helper = TikTokHelper.TikTokHelper()
    vNoob = VideoNoob()

    '''
    Debugging Tiktok Helper

    helper.getTrending(10)
    for uniqueChannelId in ['lorengray', 'zachking', 'babyariel', 'charlidamelio', 'addisonre']:
        helper.getChannelTiktoks(uniqueChannelId, count=100)
    
    for uniqueChannelId in [ 'charlidamelio']:#,'lorengray', 'zachking', 'babyariel', 'addisonre']:
        helper.getChannelTiktoks(uniqueChannelId, count=100)
     
    Debugging VideoNoob
    '''

    #vNoob.generateTikTokCompilation('charlidamelio')

    # youtube api
    scrape_channels(get_unscraped_channel_urls(limit=1))