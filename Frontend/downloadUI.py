import customtkinter as ctk
import arabic_reshaper
from bidi.algorithm import get_display
from PIL import Image
from tkinter import filedialog

#Files
from Backend.downloader import Downloader
from Backend.video import Video

class Down_UI(ctk.CTkToplevel):
    def __init__(self, master, video_obj: Video, back_app):
        self.video_obj = video_obj
        self.back_app = back_app

        super().__init__()
        self.create_child_window(master)
        self.display_thumbnail()
        self.display_details()
        self.display_location()
        self.display_qualities()
        self.display_download_button()

    def create_child_window(self, master):
        self.master = master
        self.geometry("720x360")
        self.title("Download Options")
        self.resizable(False, False)
        self.focus_set()
        self.grab_set()

        # create a frame to hold title and thumbnail
        self.top_frame = ctk.CTkFrame(self, width=700, height=200, fg_color="#1A1A1A", corner_radius=3)
        self.top_frame.pack(pady=10)

    def display_thumbnail(self):
        video_thumbnail = self.video_obj.get_image()
        image = ctk.CTkImage(light_image=video_thumbnail,
                             dark_image=video_thumbnail,
                             size=(320, 180))
        
        thumbnail_label = ctk.CTkLabel(master=self.top_frame, image=image, text="")
        thumbnail_label.place(x=10, y=10)

    def display_details(self):
        self.display_title()
        self.display_duration()
        self.display_quality()
        self.display_size()

    def display_title(self):
        title = self.video_obj.title

        if len(title) > 33:
            title = title[:30]+"...."

        title = self.modify_arabic_text(title)
        self.video_obj.title = title # update the title to the modified one to avoid issues with file naming during download

        title_label = ctk.CTkLabel(master=self.top_frame, text=title, font=("Airal", 20))
        title_label.place(x=350, y=20)

    def display_duration(self):
        duration = self.video_obj.duration

        duration_label = ctk.CTkLabel(master=self.top_frame, text=duration, font=("Arial", 13))
        duration_label.place(x=375, y=70)

        self.dispaly_detail_icon(master=self.top_frame, image_name="Duration_icon.png", x=350, y=70)
    
    def display_quality(self):
        self.quality = self.video_obj.resolution

        self.quality_label = ctk.CTkLabel(master=self.top_frame, text=self.quality, font=("Arial", 13))
        self.quality_label.place(x=375, y=100)

        self.dispaly_detail_icon(master=self.top_frame, image_name="Display_icon.png", x=350, y= 100)

    def display_size(self):
        size = self.video_obj.size

        self.size_label = ctk.CTkLabel(master=self.top_frame, text=size, font=("Arial", 13))
        self.size_label.place(x=375, y=130)

        self.dispaly_detail_icon(master=self.top_frame, image_name="Size_icon.png", x=350, y=130)

    def display_location(self):
        location = self.video_obj.location

        location_frame = ctk.CTkFrame(self, 
                                      width=400,
                                      height=32,
                                      fg_color="#1A1A1A", 
                                      corner_radius=1)
        location_frame.place(x=10, y=230)

        self.location_label = ctk.CTkLabel(master=location_frame, text=location, font=("Arial", 14))
        self.location_label.place(x=32, y=2)

        # icon
        self.dispaly_detail_icon(master=location_frame, image_name="Location_icon.png", x=5, y=1.5)

        choose_location_button = ctk.CTkButton(self,
                                               text="Browse",
                                               width=80,
                                               height=30,
                                               corner_radius=1,
                                               font=("Arial", 14),
                                               command=self.change_location)
        choose_location_button.place(x=410, y=231)
    
    def change_location(self):
        new_location = filedialog.askdirectory(title="Download location", initialdir=self.video_obj.location)

        if new_location:
            self.video_obj.location = self.video_obj.normalize_download_location(location=new_location)
            self.location_label.configure(text=self.video_obj.location)

    def display_qualities(self):

        # create a drop box to display the available qualities
        qualities = self.video_obj.get_formats()

        # convert to list of strings, but guard against empty dict
        if qualities:
            qualities_list = [str(key) for key in qualities.keys()]
        else:
            qualities_list = []

        if qualities_list:
            qualities_dropbox = ctk.CTkOptionMenu(self,
                                            values=qualities_list,
                                            width=100,
                                            height=30,
                                            corner_radius=1,
                                            font=("Arial", 13),
                                            command=self.update_resolution)
            # default to the highest available resolution (last item after sorting)
            # convert back to int for proper ordering
            try:
                sorted_vals = sorted(qualities_list, key=lambda x:int(x))
                default = sorted_vals[-1]
            except Exception:
                default = qualities_list[-1]
            qualities_dropbox.set(default)
            qualities_dropbox.place(x=10, y=300)
        else:
            # no quality options found - just show a placeholder label
            no_res_label = ctk.CTkLabel(self, text="No mp4 formats available", font=("Arial", 13))
            no_res_label.place(x=10, y=300)

        
    def update_resolution(self, choice):
        self.video_obj.update_resolution(choice)
        
        self.quality_label.configure(text=self.video_obj.resolution)
        self.size_label.configure(text=self.video_obj.size) # update the size label to reflect the new size based on the selected resolution


    def dispaly_detail_icon(self, master, image_name, x, y):

        duration_icon = self.video_obj.get_icon_image(image_name)
        duration_image = ctk.CTkImage(light_image=duration_icon, 
                                      dark_image=duration_icon,
                                      size=(20, 20))
        duration_icon_label = ctk.CTkLabel(master=master, image=duration_image, text="")
        duration_icon_label.place(x=x, y=y)

    def modify_arabic_text(self, text) -> str:
        
        reshaped_text = arabic_reshaper.reshape(text)

        bidi_text = get_display(reshaped_text)

        return bidi_text 
    
    def display_download_button(self):
        download_button = ctk.CTkButton(self,
                                       text="Download",
                                       width=100,
                                       height=30,
                                       corner_radius=1,
                                       font=("Arial", 14),
                                       command=self.start_download)
        download_button.place(x=600, y=300)

    def start_download(self):
        downloader = Downloader(self.video_obj)
        downloader.download_video()