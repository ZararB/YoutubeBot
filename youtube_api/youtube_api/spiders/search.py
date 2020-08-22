import scrapy
import json
from scrapy.shell import inspect_response
from urllib.parse import urlencode
from scrapy.utils.response import open_in_browser
from youtube_api.youtube_api.items import YoutubeSearchItem


def search_dict(partial, key):
    if isinstance(partial, dict):
        for k, v in partial.items():
            if k == key:
                yield v
            else:
                for o in search_dict(v, key):
                    yield o
    elif isinstance(partial, list):
        for i in partial:
            for o in search_dict(i, key):
                yield o


def find_value(html, key, separator='"'):
    pos_begin = html.find(key) + len(key)
    pos_end = html.find(separator, pos_begin)
    return html[pos_begin: pos_end]


def extract_channels(data):
    #TODO check what happens when there's no data - is it because youtube's antispam?
    for channel in search_dict(data, 'videoRenderer'):
        item = YoutubeSearchItem()
        item['url'] = channel['videoId']
        item['title'] = channel['title']['runs'][0]['text']
        channel_data= channel['longBylineText']['runs'][0]
        item['channel_name'] = channel_data['text']
        item['channel_url'] = channel_data['navigationEndpoint']['commandMetadata']['webCommandMetadata']['url']
        # item['views'] = channel['viewCountText']['simpleText']
        yield item


class YoutubeSearchSpider(scrapy.Spider):
    name = 'youtube'
    allowed_domains = []
    start_urls = ['https://www.youtube.com/results?search_query=tiktok']

    inner_api_key = None

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
        yield from extract_channels(data)

        if next_continuation_data is None:
            # if no 'next page', then we return None and stop the spider
            return

        params = {
            "key": self.inner_api_key
        }
        url = "https://www.youtube.com/youtubei/v1/search?" + urlencode(params)

        body_data = {
            'context':{
                'client':{
                    'visitorData':"",
                    'clientName': 'WEB',
                    'clientVersion': '2.20200814.00.00'
                },
                'request':{
                    'sessionId':{}
                },
                'adSignalsInfo':{}
            },
            'continuation':next_continuation_data
        }
        body_text = json.dumps(body_data)
        # maybe create function to generate client version to a couple days ago
        r = scrapy.Request(url,
                           body=json.dumps(body_data),
                           callback=self.parse,
                           method='POST')
        yield r

        pass
