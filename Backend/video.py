# libraries
import requests
from PIL import Image
from io import BytesIO
import os
from pathlib import Path


class Video():
    def __init__(self, info : dict, url : str = None):
        self.info = info

        self.title = info.get("title")

        self.duration = self.intialize_duration(info)

        self.resolutions = self.get_formats()
        
        # pick a default resolution: use the height field if available else take the max
        height_val = info.get("height")
        if height_val is None:
            # fall back to the highest available resolution from the formats dict
            if self.resolutions:
                height_val = max(self.resolutions.keys())
            else:
                height_val = 0

        self.resolution = f"{height_val}p"

        self.size = self.get_size()

        self.location = self.normalize_download_location(os.path.join(os.path.expanduser("~"), "Downloads"))

        self.url = url

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
        # calculate size in bytes for the currently selected resolution
        # if anything is missing we fall back to an "Unknown Size" string
        size_in_bytes = 0

        # remove the "p" from the resolution to get the height as an int
        try:
            res_key = int(self.resolution[:-1])
        except Exception:
            return "Unknown Size"

        # use dict.get in case resolutions dict is empty or missing the key
        format_id = self.resolutions.get(res_key)
        if format_id is None:
            # nothing matched the requested resolution
            return "Unknown Size"

        video_format = None
        best_audio = None

        for f in self.info.get("formats", []):

            if f.get("format_id") == format_id:
                video_format = f

            # pick the highest bitrate audio-only stream
            if f.get("vcodec") == "none" and f.get("acodec") != "none":
                if best_audio is None or f.get("abr", 0) > best_audio.get("abr", 0):
                    best_audio = f

        # if we failed to find either component just bail out
        if video_format is None or best_audio is None:
            return "Unknown Size"

        video_size = video_format.get("filesize") or video_format.get("filesize_approx") or 0
        audio_size = best_audio.get("filesize") or best_audio.get("filesize_approx") or 0

        size_in_bytes = video_size + audio_size

        # convert size to MB or GB
        if size_in_bytes > 0:
            return self.convert_Bytes(size_in_bytes)
        else:
            # if size could not be determined just set it to unknown
            return "Unknown Size"
        
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
    
    def get_icon_image(self, icon_name : str) -> Image:
        icon_location = Path(__file__).resolve().parent.parent / "Images" / icon_name

        image = Image.open(icon_location)
        return image
    
    def normalize_download_location(self, location) -> str:
        if len(location) > 50:
            return f"...."+location[-46:]
        
        return location
    

    def get_formats(self):
        # return a mapping of vertical video heights to their format_id
        formats = self.info.get("formats", [])

        resolutions = {}

        for fmt in formats:
            # only video tracks with a height and mp4 container
            if (
                fmt.get('vcodec') is not None
                and fmt.get('height') is not None
                and fmt.get('ext') == "mp4"
            ):
                height = fmt['height']
                fmt_id = fmt.get('format_id')
                if height not in resolutions and fmt_id is not None:
                    resolutions[height] = fmt_id

        return resolutions

    def update_resolution(self, choice):
        self.resolution = choice+"p"
        self.update_size()

    def update_size(self):
        # update the stored size property after the resolution has changed
        try:
            res_key = int(self.resolution[:-1])
        except Exception:
            self.size = "Unknown Size"
            return

        format_id = self.resolutions.get(res_key)
        if format_id is None:
            self.size = "Unknown Size"
            return

        video_format = None
        best_audio = None

        for f in self.info.get("formats", []):

            if f.get("format_id") == format_id:
                video_format = f

            if f.get("vcodec") == "none" and f.get("acodec") != "none":
                if best_audio is None or f.get("abr", 0) > best_audio.get("abr", 0):
                    best_audio = f

        if video_format is None or best_audio is None:
            self.size = "Unknown Size"
            return

        video_size = video_format.get("filesize") or video_format.get("filesize_approx") or 0
        audio_size = best_audio.get("filesize") or best_audio.get("filesize_approx") or 0

        full_size_in_bytes = video_size + audio_size
        self.size = self.convert_Bytes(full_size_in_bytes)
        


        


        