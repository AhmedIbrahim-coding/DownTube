import yt_dlp
import os, sys
import re
import time

class downloader:
    def __init__(self, location, video):
        self.location = location
        self.video = video

        self.progress = None
        self.downloaded = None

        self.video_total = video.total_size_bytes
        self.audio_total = 0

        self.downloaded_video = 0
        self.dowlnoaded_audio = 0

        self.speed = None
        self.is_paused = False
        self.is_canceld = False

        
    def download_video(self):
        video = self.video
        video_info = video.info
        video_title = video_info.get('title')
        video_title = re.sub(r'[^\w\s-]', '', video_title)

        # the path for downloading the video
        path = os.path.join(self.location, f"{video_title}.mp4")
        self.video_path = self.unique_path(path)

        # Download options
        opt = {
            "ffmpeg_location": self.get_ffmpeg_path(),
            "no_warnings": True,
            "quiet": True,
            "outtmpl": self.video_path,
            "format": f"bestvideo[width={video.width}][height={video.height}][ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]",
            "merge_output_format": "mp4",
            "progress_hooks": [self.progress_Hook],
        }

        try:
            with yt_dlp.YoutubeDL(opt) as downloader:
                downloader.download([video.url])
        except yt_dlp.utils.DownloadCancelled:
            print("Download is canceled by the user")

        finally:
            folder = self.location
            for file in os.listdir(folder):
                if file.endswith(".part"):
                    os.remove(os.path.join(folder, file))

    def progress_Hook(self, d):
        # exit if the downloading process is canceled
        if self.is_canceld:
            raise yt_dlp.utils.DownloadCancelled
        

        # make it pause when self.is_paused True
        while self.is_paused:
            time.sleep(0.2)

        # get the statu and store it
        status = d.get('status')

        if status == 'finished':
            # if the statu is merging the audio and video or finished, set the progress to 100
            self.progress = 100

        else :
            # get the information and fomat about the statu
            info = d.get('info_dict', {})
            fmt = d.get('format_id', "")

            # check if it's downloading audio or not
            is_audio = ("audio" in fmt) or ("m4a" in fmt)

            # get the downloaded and the full size of the current format file
            downloaded = d.get('downloaded_bytes', 0)
            total = info.get('filesize') or info.get('filesize_approx') or 0

            # if the file format is audio, set the audio_total as total that we got in the previous line
            if is_audio and self.audio_total == 0 and total > 0: # just one time 
                self.audio_total = total

            # if the file format is audio, increase the downloaded_audio, if it's not, increase the downloaded_video
            if is_audio:
                self.dowlnoaded_audio = downloaded
            else:
                self.downloaded_video = downloaded

            # store the full downloaded from the video and the audio
            total_downloaded = self.downloaded_video + self.dowlnoaded_audio

            # update the progress value if the full downloaded > 0 
            if total_downloaded > 0:
                self.progress = (total_downloaded/ self.video_total) * 100

            # get the downloading speed
            speed_in_bytes = d.get('speed')
            self.speed = self.convert_bytes(speed_in_bytes)
        

    def convert_bytes(self, bytes):
        if bytes > 1024:
            KB = bytes / 1024
            if KB > 1024:
                MB = KB / 1024
                if MB > 1024:
                    GB = MB / 1024
                    return f"{GB:.2f}GB/s"
                else:
                    return f"{MB:.2f}MB/s"
            else:
                return f"{KB:.2f}KB/s"
        else:
            return f"{bytes:.2f}B/s"
        
    def get_ffmpeg_path(self):
        if hasattr(sys, "_MEIPASS"):
            return os.path.join(sys._MEIPASS, "FFmpeg\\bin\\ffmpeg.exe")
        return os.path.join(os.getcwd(), "FFmpeg", "bin")
        
    
    def unique_path(self, path):
        # split the path to base and exit
        base, ext = os.path.splitext(path)

        # avoid repititve names
        counter = 1
        while os.path.isfile(path):
            path = f"{base}({counter}){ext}"
            counter += 1

        # return the final path form
        return path
