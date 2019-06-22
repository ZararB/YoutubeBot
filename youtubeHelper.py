
import subprocess


class YoutubeHelper:

    def __init__(self):
        pass

    def upload_video(self, filename, title, description):

        """Uploads video with given metadata.
        """
        subprocess.run(["python", "youtube.py", "--file", filename, ])
