import scrapy
import json
from scrapy.shell import inspect_response
from urllib.parse import urlencode
from scrapy.utils.response import open_in_browser
from youtube_api.youtube_api.items import YoutubeVideo


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
    for channel in search_dict(data, 'gridVideoRenderer'):
        item = YoutubeVideo()
        item['url'] = channel['videoId']
        item['title'] = channel['title']['simpleText']
        item['thumbnail'] = channel['thumbnail']['thumbnails'][0]
        item['views'] = channel['viewCountText']['simpleText']
        yield item


class YoutubeSpider(scrapy.Spider):
    name = 'youtube'
    allowed_domains = []
    start_urls = ['https://www.youtube.com/user/PewDiePie/videos']

    def parse(self, response):
        # inspect_response(response, self)
        is_html = response.xpath("//script").get()
        print(response.body)
        if is_html is not None:
            # if it's the first page then we scrape the html for
            data = json.loads(find_value(response.body.decode("utf-8"), 'window["ytInitialData"] = ', '\n').rstrip(';'))
        else:
            data = json.loads(response.body)

        next_continuation_data = next(search_dict(data, 'nextContinuationData'), None)

        yield from extract_channels(data)

        if next_continuation_data is None:
            # if no 'next page', then we return None and stop the spider
            return

        params = {
            "ctoken": next_continuation_data["continuation"],
            "continuation": next_continuation_data["continuation"],
            "itct": next_continuation_data["clickTrackingParams"]
        }
        url = "https://www.youtube.com/browse_ajax/?" + urlencode(params)

        headers = {'X-YouTube-Client-Name': '1',
                   'X-YouTube-Client-Version': '2.20200207.03.01'}
        yield scrapy.Request(url, headers=headers, callback=self.parse)

        pass
