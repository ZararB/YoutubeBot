# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class YoutubeVideo(scrapy.Item):
    title = scrapy.Field()
    url = scrapy.Field()
    channel_url = scrapy.Field()
    thumbnail = scrapy.Field()
    description = scrapy.Field()
    views = scrapy.Field()
    uploaded_at = scrapy.Field()

    pass


class YoutubeChannelItem(scrapy.Item):
    title = scrapy.Field()
    url = scrapy.Field()
    channel_name = scrapy.Field()
    channel_url = scrapy.Field()
    description = scrapy.Field()
    views = scrapy.Field()
    searchterm_id = scrapy.Field()
    pass
