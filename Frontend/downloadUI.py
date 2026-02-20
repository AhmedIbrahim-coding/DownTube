import customtkinter as ctk
import arabic_reshaper
from bidi.algorithm import get_display

class Down_UI(ctk.CTkToplevel):
    def __init__(self, master, video_obj):
        self.video_obj = video_obj

        super().__init__()
        self.create_child_window(master)
        self.display_thumbnail()
        self.display_details()
        self.display_location


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

        title_label = ctk.CTkLabel(master=self.top_frame, text=title, font=("Airal", 20))
        title_label.place(x=350, y=20)

    def display_duration(self):
        duration = self.video_obj.duration

        duration_label = ctk.CTkLabel(master=self.top_frame, text=duration, font=("Arial", 13))
        duration_label.place(x=375, y=70)

    def display_quality(self):
        quality = self.video_obj.resolution

        quality_label = ctk.CTkLabel(master=self.top_frame, text=quality, font=("Arial", 13))
        quality_label.place(x=375, y=100)

    def display_size(self):
        size = self.video_obj.size

        size_label = ctk.CTkLabel(master=self.top_frame, text=size, font=("Arial", 13))
        size_label.place(x=375, y=130)

    def display_location(self):
        location = self.video_obj.location

        location_frame = ctk.CTkFrame(self,
                                      width=400,
                                      height=32,
                                      fg_color="#1A1A1A", 
                                      corner_radius=1)
        location_frame.place(x=10, y=230)

        self.location_label = ctk.CTkLabel(master=location_frame, text=location, font=("Arial", 12))
        self.location_label.place(x=32, y=2)


    def modify_arabic_text(self, text) -> str:
        
        reshaped_text = arabic_reshaper.reshape(text)

        bidi_text = get_display(reshaped_text)

        return bidi_text 