
import subprocess



class RecordNoob():

    def __init__(self):
        pass

    def record_game(self):
        # Record screen
        subprocess.run(["ffmpeg", "-f", "x11grab", "-s","1920x1080","-t", "30", "-i", ":0.0", "output.mkv"])
