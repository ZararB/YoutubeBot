from database.models.base import Base
from sqlalchemy import Column, Integer, String, ForeignKey
from database.models.youtube_channel import YoutubeChannel


class YoutubeVideo(Base):
    __tablename__ = 'YoutubeVideos'

    Id = Column(Integer, primary_key=True)
    VideoUrl = Column(String)
    ChannelId = Column(Integer, ForeignKey(YoutubeChannel.Id))
    Title = Column(String)
    Views = Column(String)
    Description = Column(String, nullable=True)
    ThumbnailUrl = Column(String, nullable=True)
    ThumbnailFileLocation = Column(String, nullable=True)
    UploadedAt = Column(String)

    def __init__(self,
                 video_url=None,
                 channel_id=None,
                 title=None,
                 views=None,
                 description=None,
                 thumbnail_url=None,
                 thumbnail_file_locatiton=None,
                 uploaded_at=None):

        self.VideoUrl = video_url
        self.ChannelId = channel_id
        self.Title = title
        self.Views = views,
        self.Description = description,
        self.ThumbnailUrl = thumbnail_url,
        self.ThumbnailFileLocation = thumbnail_file_locatiton,
        self.UploadedAt = uploaded_at
        pass
