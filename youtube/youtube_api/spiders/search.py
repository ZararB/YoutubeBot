import scrapy
import json
from urllib.parse import urlencode, quote_plus
from youtube.youtube_api.items import YoutubeChannelItem
from youtube.youtube_api.spiders.helper import search_dict, find_value
from database.youtube import create_searchterm


class YoutubeSearchSpider(scrapy.Spider):
    name = 'youtube'
    allowed_domains = []
    base_url = 'https://www.youtube.com/results?search_query='
    start_urls = []

    inner_api_key = None

    searchterm_id = None

    def __init__(self, search_term=None):
        if search_term is None:
            raise ValueError("Search spider needs to be provided a string search term")

        self.start_urls = [self.base_url + quote_plus(search_term)]
        self.searchterm_id = create_searchterm(term=search_term)
        pass

    def parse(self, response):
        is_html = response.xpath("//script").get()

        if is_html is not None:
            # if it's the first page then we scrape the html for
            raw_data = find_value(response.body.decode("utf-8"), 'window["ytInitialData"] = ', '\n').rstrip(';')
            data = json.loads(find_value(response.body.decode("utf-8"), 'window["ytInitialData"] = ', '\n').rstrip(';'))
            raw_config = find_value(response.body.decode("utf-8"), '(function() {var configs = ', '\n')
            config = json.loads(raw_config.split(';')[0])
        else:
            data = json.loads(response.body)

        next_continuation_data = next(search_dict(data, 'token'), None)
        if self.inner_api_key is None:
            self.inner_api_key = next(search_dict(config, 'innertubeApiKey'), None)
        yield from self.extract_channels(data)

        if next_continuation_data is None:
            # TODO N add default number of pages it will scrape w/ parameter to override(eg default is 2 pages so after 2 pages it stops, but if parameter is provided it will try to scrape that many pages
            # if no 'next page', then we return None and stop the spider
            return

        params = {
            "key": self.inner_api_key
        }
        url = "https://www.youtube.com/youtubei/v1/search?" + urlencode(params)

        body_data = {
            'context': {
                'client': {
                    'visitorData': "",
                    'clientName': 'WEB',
                    'clientVersion': '2.20200814.00.00'
                },
                'request': {
                    'sessionId': {}
                },
                'adSignalsInfo': {}
            },
            'continuation': next_continuation_data
        }
        body_text = json.dumps(body_data)
        # maybe create function to generate client version to a couple days ago
        r = scrapy.Request(url,
                           body=json.dumps(body_data),
                           callback=self.parse,
                           method='POST')
        yield r

        pass

    def extract_channels(self, data):
        # TODO check what happens when there's no data - is it because youtube's antispam?
        for channel in search_dict(data, 'videoRenderer'):
            item = YoutubeChannelItem()
            item['url'] = channel['videoId']
            item['title'] = channel['title']['runs'][0]['text']
            channel_data = channel['longBylineText']['runs'][0]
            item['channel_name'] = channel_data['text']
            item['channel_url'] = channel_data['navigationEndpoint']['commandMetadata']['webCommandMetadata']['url']
            item["searchterm_id"] = self.searchterm_id
            item['views'] = channel['viewCountText']['simpleText']
            yield item
