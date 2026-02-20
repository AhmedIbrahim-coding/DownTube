# libraries
import requests
from PIL import Image
from io import BytesIO
import os


class Video():
    def __init__(self, info : dict):
        self.info = info

        self.title = info.get("title")

        self.duration = self.intialize_duration(info)
        
        self.size = self.get_size()

        self.resolution = f"{info.get("width")}X{info.get("height")}"

        self.location = os.path.join(os.path.expanduser("~"), "Downloads")
        print(self.location)


    def intialize_duration(self, info) -> str:
        time_in_sec = info.get("duration")
        
        if time_in_sec < 60:
            # e.g. 0:09
            return f"0:{time_in_sec:02d}"
        
        elif time_in_sec < 3600:
            minutes = time_in_sec // 60
            seconds = time_in_sec % 60
            # e.g. 03:12
            return f"{minutes:02d}:{seconds:02d}"
        
        else:
            hours = time_in_sec // 3600
            minutes = (time_in_sec % 3600) // 60
            seconds = time_in_sec % 60
            # e.g. 1:03:20
            return f"{hours}:{minutes:02d}:{seconds:02d}"


    def get_size(self) -> str:
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
            return self.convert_Bytes(size_in_bytes)
        else:
            # if size could not be determined just set it to unknown
            return" Unknown Size"
        
    def convert_Bytes(self, size_in_bytes : int) -> str:
            
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
                
    def get_image(self) -> Image:
        # gitting the image from the thumbnail url
        response = requests.get(self.info.get("thumbnail"))

        # store the image as bytes
        image_bytes = response.content

        # convert bytes to a PhotoImage
        image = Image.open(BytesIO(image_bytes))
        
        return image
            
        


        