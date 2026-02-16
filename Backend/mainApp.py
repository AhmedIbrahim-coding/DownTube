import time
from threading import Thread
import yt_dlp

class BackApp():
    def __init__(self, frontApp):
        self.frontApp = frontApp


    def check_existance(self, url):
        if not self.frontApp.is_check:
            get_info_thread = Thread(target=self.get_video_info, args=(url,), daemon=True)
            get_info_thread.start()

            loading_thread = Thread(target=self.frontApp.display_loading_message, daemon=True)
            loading_thread.start()

    def get_video_info(self, url : str):
        self.frontApp.is_check = True
        
        try:
            if not url.startswith("https://www.youtube.com/watch?v="):
                raise Exception

            options = {
            'quiet': True,
            'no_warnings': True,
            'skip_download': True,
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]',
            }
        
            with yt_dlp.YoutubeDL(options) as ydl:
                info = ydl.extract_info(url=url, download=False)
                
                if not info.get("duration"):
                    raise Exception

            self.frontApp.is_check = False
        except:
            self.frontApp.is_check = False
            time.sleep(0.5)
            self.frontApp.display_error_message(message="Invalid URL.")
