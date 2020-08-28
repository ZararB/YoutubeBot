from youtube.youtube_api.scraper_api import search_youtube
from youtube.youtube_api.scraper_api import scrape_channel
from database.youtube import get_unscraped_channel_urls

if __name__ == '__main__':
    scrape_channel(get_unscraped_channel_urls(limit=1))
    print(get_unscraped_channel_urls(limit=1))
