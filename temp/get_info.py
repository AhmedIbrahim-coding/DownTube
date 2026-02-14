import yt_dlp
import requests
from PIL import Image
from io import BytesIO

class video:
    def __init__(self, url):
        self.url = url
        self.info = None
        self.duration = None
        self.size = None
        self.height = None
        self.width = None
        self.total_size_bytes = None
        '''self.formats = []'''

    def getInformations(self):
        options = {
            'quiet': True,
            'no_warnings': True,
            'skip_download': True,
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]',
        }
        with yt_dlp.YoutubeDL(options) as ydl:
            info = ydl.extract_info(self.url, download=False)
            self.info = info
            # set video as the best quality based on height and width
            if self.info['height'] and self.info['width']:
                self.height = self.info['height']
                self.width = self.info['width']
            return self.info
        
        
    
    def GetImage(self):
        # gitting the image from the thumbnail url
        response = requests.get(self.info['thumbnail'])

        # store the image as bytes
        image_bytes = response.content

        # convert bytes to a PhotoImage
        image = Image.open(BytesIO(image_bytes))
        
        return image

    def getDuration(self):
        duration = self.info['duration']
        video_time = ""
        
        if duration < 60:
             # e.g. 0:45
            video_time = f"0:{duration:02d}"
            
        elif duration < 3600:
             # e.g. 12:05
            video_time = f"{duration//60}:{duration%60:02d}"
            
        else:
            # e.g. 2:05:30
            # The logic is the same, just cleaner to read
            hours = duration // 3600
            minutes = (duration % 3600) // 60
            seconds = duration % 60
            video_time = f"{hours}:{minutes:02d}:{seconds:02d}"

        self.duration = video_time

    def getSize(self):
        # set an initial size of 0 bytes
        size_in_bytes = 0

        # git the size from the info dict
        if "requested_formats" in self.info:
            video_fmt = self.info['requested_formats'][0]
            audio_fmt = self.info['requested_formats'][1]
            
            video_size = video_fmt.get('filesize') or video_fmt.get('filesize_approx')
            audio_size = audio_fmt.get('filesize') or audio_fmt.get('filesize_approx')

            size_in_bytes = video_size + audio_size
        else:
            fmt = self.info
            size_in_bytes = fmt.get('filesize') or fmt.get('filesize_approx')

        # convert size to MB or GB
        if size_in_bytes > 0:
            self.size = self.convertBytes(size_in_bytes)
        else:
            # if size could not be determined just set it to unknown
            self.size = " Unknown Size"

        self.total_size_bytes = size_in_bytes

    def convertBytes(self, size_in_bytes):
            
            KB = size_in_bytes / (1024)
            if KB < 1000:
                return f"{KB:.2f} KB"
            else:
                MB = KB / 1024
                if MB < 1000:
                    return f"{MB:.2f} MB"
                else:
                    GB = MB / 1024
                    return f"{GB:.2f} GB"
    
    '''            
    def get_Qualities(self):
        formats = self.info.get("formats")
        qualitites = []
        for f in formats:
            if f.get("height") and f.get("width") and f.get("vcodec") and f.get("height") > 144 and int(f['format_id']) >= 395:
                self.formats.append(f)
                resolution = f.get("resolution")
                qualitites.append(resolution)
        print(self.formats)
        return qualitites'''