from database.connection import Session
from database.models.youtube_searchterm import YoutubeSearchTerm
from database.models.youtube_channel import YoutubeChannel
from database.models.youtube_video import YoutubeVideo
from sqlalchemy.sql import func


def create_searchterm(term):
    """
    Adds the search term to the database.
    @param: channel: the search term to be added
    @type: channel: bar
    @return: returns integer representing the id of the added item
    @rtype: int
    """
    record = YoutubeSearchTerm(term=term)
    session = Session()
    session.add(record)
    session.commit()

    return record.Id
    pass


def create_channel(channel):
    """
    @param: scraped channel to be added to the database
    @type: scrapy.item
    @return: None
    """

    record = YoutubeChannel(
        url=channel["channel_url"],
        nickname=channel["channel_name"],
        searchterm=channel["searchterm_id"],
        searchterm_views=channel["views"]
    )
    session = Session()

    # check if channel exists already and is not deleted
    exists = session.query(YoutubeChannel.Id).filter(YoutubeChannel.Url == record.Url).scalar() is not None

    # if it doesn't exist -> add it to the database
    if not exists:
        session.add(record)
        session.commit()
    pass


def get_channel_id_by_url(channel_url):
    session = Session()

    # check if channel exists already and is not deleted
    id = session.query(YoutubeChannel.Id).filter(YoutubeChannel.Url == channel_url).scalar()

    if id is None:
        raise Exception("Channel does not exist")
    else:
        return id
    pass


def channel_scraped_at(channel_url):
    session = Session()

    # get channel
    record = YoutubeChannel(url=channel_url,
                            scraped_at=func.now())
    channel = session.query(YoutubeChannel).filter(YoutubeChannel.Url == channel_url).first()

    # update channel ScrapedAt field
    channel.ScrapedAt = record.ScrapedAt
    session.commit()
    pass


def get_unscraped_channel_urls(limit=None):
    """

    @param limit: an integer representing how many results you would like to receive back
    @return: a list of unscraped channel urls
    """
    session = Session()
    # define unscraped channel criteria
    query = session.query(YoutubeChannel.Url). \
        filter(YoutubeChannel.ScrapedAt == None). \
        filter(YoutubeChannel.DeletedAt == None)

    if limit is None:
        results = query.all()
    else:
        results = query.limit(limit).all()

    return [value for value, in results]  # convert tuple to list
    pass


def create_youtube_video(video):
    """
    Adds scraped data to database
      @param: scraped video to be added to the database
      @type: scrapy.item
      @return: None
      """
    record = YoutubeVideo(
        video_url=video["url"],
        channel_id=get_channel_id_by_url(video["channel_url"]),
        title=video["title"],
        views=video["views"],
        description=["description"],
        thumbnail_url=["thumbnail"],
        uploaded_at=["uploaded_at"]
    )
    session = Session()

    # check if channel exists already and is not deleted
    exists = session.query(YoutubeVideo.Id).filter(YoutubeVideo.VideoUrl == record.VideoUrl,
                                                   YoutubeVideo.ChannelId == record.ChannelId).scalar() is not None

    # if it doesn't exist -> add it to the database
    if not exists:
        session.add(record)
        session.commit()

    pass
