# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import database.youtube as db
from youtube.youtube_api.items import YoutubeChannelItem, YoutubeVideo


class YoutubeApiPipeline:
    def process_item(self, item, spider):
        return item


class DatabasePipeline:
    def process_item(self, item, spider):
        if isinstance(item, YoutubeChannelItem):
            db.create_channel(item)
        if isinstance(item, YoutubeVideo):
            db.create_youtube_video(item)
        return item
