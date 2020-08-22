import subprocess

class youtubeHelper():


    def __init__(self):
        
        pass

    def upload_video(self, channel, filepath, title, description):


        channel_auth = "~/YoutubeBot/auths/" + channel + ".json"
        original_filepath = "~/YoutubeBot/auths/upload_video.py-oauth2.json"
        subprocess.run(["rm", original_filepath])
        subprocess.run(["cp", channel_auth, original_filepath])
        subprocess.run(["python3", "upload_video.py", 
        "--file="+filepath, "--title="+title, "--description="+description, "--noauth_local_webserver"])

        


