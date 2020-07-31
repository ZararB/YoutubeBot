# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class YoutubeVideo(scrapy.Item):
    title = scrapy.Field()
    url = scrapy.Field()
    thumbnail = scrapy.Field()
    description = scrapy.Field()
    views = scrapy.Field()
    timestamp = scrapy.Field()

    pass
