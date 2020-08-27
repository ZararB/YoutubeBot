from scrapy.crawler import CrawlerProcess
from youtube.youtube_api.spiders.search import YoutubeSearchSpider
from youtube.youtube_api.spiders.channel import ChannelSpider
from scrapy.settings import Settings


def search_youtube(search_term):
    # given a search term, this will scrape youtube for
    crawler_settings = Settings()
    crawler_settings.set('DOWNLOAD_DELAY', 1)
    crawler_settings.set('ITEM_PIPELINES',
                         {'youtube.youtube_api.pipelines.DatabasePipeline': 500})
    crawler_settings.set('USER_AGENT',
                         'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_6; en-en) AppleWebKit/533.19.4 (KHTML, like Gecko) Version/5.0.3 Safari/533.19.4')

    process = CrawlerProcess(crawler_settings)

    process.crawl(YoutubeSearchSpider, search_term=search_term)
    process.start()

    pass


def scrape_channel(channel_urls):
    crawler_settings = Settings()
    crawler_settings.set('DOWNLOAD_DELAY', 1)
    crawler_settings.set('ITEM_PIPELINES',
                         {'youtube.youtube_api.pipelines.DatabasePipeline': 500})
    crawler_settings.set('USER_AGENT',
                         'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_6; en-en) AppleWebKit/533.19.4 (KHTML, '
                         'like Gecko) Version/5.0.3 Safari/533.19.4')

    process = CrawlerProcess(crawler_settings)

    process.crawl(ChannelSpider, channel_urls=channel_urls)
    process.start()

    pass
