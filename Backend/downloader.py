import yt_dlp
import os

class Downloader():
    def __init__(self, video_obj):
        self.video_obj = video_obj

        print(video_obj.resolution, "\n", video_obj.location)


    def download_video(self):
        resolution = int(self.video_obj.resolution[:-1]) # remove the "p" from the resolution to get the height
        video_format = self.video_obj.resolutions[resolution] # get the format id that matches the resolution
        path = self.unique_path(self.video_obj.location)

        options = {
            'quiet': True,
            'no_warnings': True,
            'format': f'{video_format}+bestaudio[ext=m4a]/best[ext=mp4]',
            'outtmpl': f'{path}/%(title)s.%(ext)s',
        }
        
        with yt_dlp.YoutubeDL(options) as ydl:
            ydl.download([self.video_obj.url])

    def unique_path(self, path):
        # split the path to base and exit
        base, ext = os.path.splitext(path)

        # avoid repititve names
        counter = 1
        while os.path.isfile(path):
            path = f"{base}({counter}){ext}"
            counter += 1

            print(path)

        # return the final path form
        return path