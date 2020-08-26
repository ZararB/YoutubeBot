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

    vNoob.generateTikTokCompilation('charlidamelio')


