import scrapy
import json
from urllib.parse import urlencode, quote_plus
from youtube.youtube_api.items import YoutubeVideo
from youtube.youtube_api.spiders.helper import search_dict, find_value
from database.youtube import channel_scraped_at


class ChannelSpider(scrapy.Spider):
    name = 'channel'
    allowed_domains = []
    start_urls = ['https://www.youtube.com/user/PewDiePie/videos']
    total_scraped = 0
    base_url = 'https://www.youtube.com'
    channel_requests = None
    number_of_videos = 20 # Default number of videos scraped

    def __init__(self, channel_urls=None, number_of_videos=None):
        """

        @param channel_urls: list of channel urls to visit and scrape
        @type list

        @param number_of_videos: the number of videos you want to scrape from this channel(note: most likely only works
        """
        if channel_urls is None:
            raise ValueError("Search spider needs to be passed a channel_urls list")
        if number_of_videos is not None:
            self.number_of_videos = number_of_videos

        self.channel_requests = map(self.channel_url_to_request, channel_urls)
        pass

    def channel_url_to_request(self, channel_url):
        return scrapy.Request(url=self.base_url + channel_url + '/videos',
                              meta={'channel_url': channel_url})
        pass

    def start_requests(self):
        return self.channel_requests
        pass

    def parse(self, response):
        is_html = response.xpath("//script").get()
        print(response.body)
        if is_html is not None:
            # if it's the first page then we scrape the html for
            data = json.loads(find_value(response.body.decode("utf-8"), 'window["ytInitialData"] = ', '\n').rstrip(';'))
        else:
            data = json.loads(response.body)

        next_continuation_data = next(search_dict(data, 'nextContinuationData'), None)

        yield from self.extract_channels(data, response)

        if (next_continuation_data is None) or (self.total_scraped >= 20):
            # if no 'next page' or if we scraped x amount of records, then we return None
            # add timestamp to show channel has been scraped
            channel_scraped_at(response.meta["channel_url"])
            return

        params = {
            "ctoken": next_continuation_data["continuation"],
            "continuation": next_continuation_data["continuation"],
            "itct": next_continuation_data["clickTrackingParams"]
        }
        url = "https://www.youtube.com/browse_ajax/?" + urlencode(params)

        headers = {'X-YouTube-Client-Name': '1',
                   'X-YouTube-Client-Version': '2.20200207.03.01'}
        # TODO N maybe have a X_
        yield scrapy.Request(url, headers=headers, callback=self.parse)

        pass

    def extract_channels(self, data, response):
        # TODO check what happens when there's no data - is it because youtube's antispam?
        for video in search_dict(data, 'gridVideoRenderer'):
            self.total_scraped += 1
            item = YoutubeVideo()
            item['channel_url'] = response.meta["channel_url"]
            item['url'] = video['videoId']
            item['title'] = video['title']['runs'][0]['text']
            item['thumbnail'] = video['thumbnail']['thumbnails'][0]['url']
            item['views'] = video['viewCountText']['simpleText']
            item['uploaded_at'] = video['publishedTimeText']['simpleText']
            yield item
