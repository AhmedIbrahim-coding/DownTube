import customtkinter as ctk
from get_info import video
import threading
from PIL import Image
from tkinter import filedialog, font as tkFont
import tkinter as tk
import os, sys
from Downloader import downloader

# a func to import any item as a code or exe file
def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):  # Running as EXE
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)  # Running normally

# set the appearance automatically to dark
ctk.set_appearance_mode("Dark")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("DownTube")
        self.geometry("500x200")
        self.resizable(False, False)
        self.video_link = None
        self.video_info = None
        self.download_location = os.path.join(os.path.expanduser("~"), "Downloads")


        # type my name well, i mean i am gonna do that you know (-_-)
        my_name = ctk.CTkLabel(self, text="By/ Ahmed Ibrahim", font=("Arial", 12))
        my_name.place(x=10, y=170)

        # set an icon for the app
        self.iconbitmap(resource_path("DownTube_icon.ico"))


        # Link entry
        self.linkEntry = ctk.CTkEntry(self,
                                       width=450,
                                       height=30,
                                       placeholder_text="Enter the video link here...",
                                       corner_radius=3,
                                       font=("Arial", 14))
        self.linkEntry.pack(pady=20)

        # add a menu when right click on link entry
        self.menu = tk.Menu(self, 
                            tearoff=0,
                            fg="white",
                            bg="#1f1f1f",
                            bd=0,
                            activebackground="#3d3d3d",
                            activeforeground="white",
                            font=tkFont.Font(family="Arial", size=10))
        
        # add commands to the menu {copy, past, cut}
        self.menu.add_command(label="Past", command=lambda: self.linkEntry.insert("insert", self.clipboard_get()))
        self.menu.add_command(label="Copy", command=lambda: self.clipboard_append(self.linkEntry.get()))
        self.menu.add_command(label="Cut", command=lambda: (self.clipboard_clear(), self.clipboard_append(self.linkEntry.get()), self.linkEntry.delete(0, "end")))

        self.linkEntry.bind("<Button-3>",self.show_menu) # make it appears when the user hit the right lick button on the entry field
        
        # start download button
        self.download_button = ctk.CTkButton(self,
                                             text="Download",
                                             width=80,
                                             height=30,
                                             corner_radius=3,
                                             font=("Arial", 14),
                                             command=self.check_excistance)
        self.download_button.pack(pady=10)

        # create a variable to hold error text
        self.error_text = None

    def show_menu(self, event):
        self.menu.tk_popup(event.x_root, event.y_root)
        self.menu.grab_release()
    
    def check_excistance(self):
        # remove previous error text if exists
        if(self.error_text):
            self.error_text.destroy()

        # We just get the text here. The validation happens in the thread now.
        self.video_link = self.linkEntry.get()
        
        # Check if the link is empty
        if(not self.video_link):
            self.main_error_massage("Please enter a video link.")
            return
        # 1. Open the window immediately
        self.download_options()
        self.error_text = None 
    
    def download_options(self):
        window = self.download_window = ctk.CTkToplevel(self)
        window.title("Download Options")
        window.geometry("720x360")
        window.resizable(False, False)
        window.grab_set()  # Make this window modal
        window.focus_set()

        # write a temorary lable to show that the download is being prepared
        self.temp_label_massage = ctk.CTkLabel(window, text="Preparing download....", font=("Arial", 32))
        self.temp_label_massage.place(relx=0.5, rely=0.5, anchor='center')
        
        new_video = video(self.video_link) # crate a new video object
        
        # 2. Start the thread (Fixed the tuple syntax here too)
        threading.Thread(target=self.fetch_video_info, args=(new_video,)).start()


    def fetch_video_info(self, video_obj):
            try:
                # 1. Get the info
                video_info = video_obj.getInformations()
                
                # 2. Check Is it actually a video?
                is_live = video_info.get('is_live', False)
                duration = video_info.get('duration')

                if not duration and not is_live:
                    raise Exception("Link is a Page, not a Video")

                # 3. If we passed the check, save it and update GUI
                self.video_info = video_info
                self.after(0, self.display_video_info, video_obj)
            except Exception:
                # 4. Display the error on the main screen
                self.after(0, self.handle_error)

    def handle_error(self):
        # This function runs on the Main Thread when triggered by the background thread
        self.main_error_massage("Invalid URL. Please try again.")
        
        if self.download_window:
            self.download_window.destroy()

    def main_error_massage(self, massage):
            # display error message
            self.error_text = ctk.CTkLabel(self,
                                           text=massage,
                                           text_color="red",
                                           font=("Arial", 12))
            self.error_text.place(relx=0.5, y=150, anchor='center')

    def display_video_info(self, video_obj):
        # create a local reference to the download window
        window = self.download_window

        # Clear previous widgets
        for widget in window.winfo_children():
            widget.destroy()

        # create a frame to hold title and thumbnail
        top_frame = ctk.CTkFrame(window, width=700, height=200, fg_color="#1A1A1A", corner_radius=3)
        top_frame.pack(pady=10)

        # display video thumbnail
        video_thmb = video_obj.GetImage()
        image = ctk.CTkImage(light_image= video_thmb,
                             dark_image= video_thmb,
                             size=(320, 180))
        thumbnail_label = ctk.CTkLabel(top_frame, image=image, text="")
        thumbnail_label.place(x=10, y=10)

        # display video title
        title = self.video_info['title']
        if len(title) > 33:
            title = title[:30] + " ..."
        video_title = ctk.CTkLabel(top_frame,
                                    text=title,
                                    font=("Arial", 20))
        video_title.place(x=350, y=20)

        # display video duration
        pil_duration_icon = Image.open(resource_path("Duration_icon.png"))
        duration_icon = ctk.CTkImage(light_image= pil_duration_icon,
                                     dark_image= pil_duration_icon,
                                     size=(20, 20))
        duration_icon_label = ctk.CTkLabel(top_frame, image=duration_icon, text="")
        duration_icon_label.place(x=350, y=70)

        video_obj.getDuration()
        duration_label = ctk.CTkLabel(top_frame,
                                      text=video_obj.duration,
                                      font=("Arial", 13))
        duration_label.place(x=375, y=70)

        # display video file size
        pil_size_icon = Image.open(resource_path("Size_icon.png"))
        size_icon = ctk.CTkImage(light_image= pil_size_icon,
                                 dark_image= pil_size_icon,
                                 size=(20, 20))
        size_icon_label = ctk.CTkLabel(top_frame, image=size_icon, text="")
        size_icon_label.place(x=350, y=100)

        video_obj.getSize()
        size_label = ctk.CTkLabel(top_frame,
                                  text=video_obj.size,
                                  font=("Arial", 13))
        size_label.place(x=375, y=100)

        # display video quality
        pil_display_icon = Image.open(resource_path("Display_icon.png"))
        display_icon = ctk.CTkImage(light_image= pil_display_icon,
                                    dark_image= pil_display_icon,
                                    size=(20, 20))
        display_icon_label = ctk.CTkLabel(top_frame, image=display_icon, text="")
        display_icon_label.place(x=350, y=130)

        quality_label = ctk.CTkLabel(top_frame,
                                     text=f"{video_obj.width}x{video_obj.height}" if video_obj.height and video_obj.width else "Unknown Quality",
                                     font=("Arial", 13))
        quality_label.place(x=375, y=130)


        # Choose download location path and button_browse
        location_frame = ctk.CTkFrame(window, width=400, 
                                      height=32, 
                                      fg_color="#1A1A1A", 
                                      corner_radius=1)
        location_frame.place(x=10, y=230)

        # display location icon
        pil_location_icon = Image.open(resource_path("Location_icon.png"))
        location_icon = ctk.CTkImage(light_image= pil_location_icon,
                                     dark_image= pil_location_icon,
                                     size=(25, 25))
        location_icon_label = ctk.CTkLabel(location_frame, image=location_icon, text="")
        location_icon_label.place(x=5, y=1.5)

        # display current download location & make it accessible for other methods
        self.location_label = ctk.CTkLabel(location_frame, text=self.download_location, font=("Arial", 14))
        self.location_label.place(x=32, y=2)

        self.choose_location_button = ctk.CTkButton(window,
                                               text="Browse",
                                               width=80,
                                               height=30,
                                               corner_radius=1,
                                               font=("Arial", 14),
                                               command=self.choose_location)
        self.choose_location_button.place(x=410, y=231)
        '''
        # Choose Quality drop box
        opt = video_obj.get_Qualities() # get the resolutions list
        self.opt_box = ctk.CTkComboBox(window, 
                                       values=opt, 
                                       height=30, 
                                       width=150, 
                                       command=lambda selected_value: self.choose_quality(video_obj, selected_value))
        self.opt_box.place(x=20, y=310)
        self.opt_box.set(opt[-1]) # set the heighst quality as default
        '''

        # Download button
        self.start_download_button = ctk.CTkButton(window,
                                              text="Start",
                                              width=100,
                                              height=30,
                                              corner_radius=3,
                                              font=("Arial", 16),
                                              command=lambda: self.DownloadVideo(video_obj))
        self.start_download_button.place(x=600, y=310)

    def choose_location(self):
        # get the download path from the user
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            # set the download locatoin variable
            self.download_location = folder_selected
            self.location_label.configure(text=self.download_location)
    
    """
    def choose_quality(self, choise, video_obj):
        choise = self.opt_box.get()
        print(choise)
    """

    def DownloadVideo(self, video_obj):
        # if the download button exists, destroy it
        if self.start_download_button.winfo_exists():
            self.start_download_button.destroy()


        # create a progress label
        self.progrss_label = ctk.CTkLabel(self.download_window ,text="")
        self.progrss_label.place(relx=0.5, y=310, anchor="center")

        # create a progress bar
        self.progress_bar = ctk.CTkProgressBar(self.download_window, width=400, height=5, corner_radius=3)
        self.progress_bar.place(relx=0.5, y=320, anchor="center")
        self.progress_bar.set(0)

        # display a speed label
        self.speed_label = ctk.CTkLabel(self.download_window, text="")
        self.speed_label.place(x=570, y=305)

        # crate a new downloader object
        new_downloader = downloader(self.download_location, video_obj)

        # make the downloading process cancel when the user closes the download window
        self.download_window.protocol("WM_DELETE_WINDOW", lambda: self.on_close(new_downloader))

        # start the downloading process as a thread to run in the background
        self.download_thread = threading.Thread(target=self.Downloading_prosses,
                                                args=(new_downloader,),
                                                daemon=True
                                                )
        self.download_thread.start()
        self.after(0, self.update_progress, new_downloader)


        # Pause Button
        pil_pause_icon = Image.open(resource_path("Pause_icon.png"))
        pil_continue_icon = Image.open(resource_path("Continue_icon.png"))
        self.pause_icon = ctk.CTkImage(light_image=pil_pause_icon,
                                       dark_image=pil_pause_icon,
                                       size=(15, 15))
        self.continue_icon = ctk.CTkImage(light_image=pil_continue_icon,
                                          dark_image=pil_continue_icon,
                                          size=(15,15))
        self.pause_button = ctk.CTkButton(self.download_window, 
                                     width=35, 
                                     height=30, 
                                     corner_radius=0, 
                                     text="",
                                     fg_color="#1F6AA5",
                                     hover_color="#1F466D",
                                     image=self.pause_icon, 
                                     command=lambda:self.Pause_process(new_downloader))
        self.pause_button.place(relx=0.5, y=340, anchor="center")

    def on_close(self, downloader_obj):
        # if the video still downloading cancel it
        try:
            if downloader_obj.progress and downloader_obj.progress < 100:
                downloader_obj.is_canceld = True
        except Exception as e:
            print(f"Error setting cancel flag: {e}")
        
        # destroy the window as normal
        try:
            self.download_window.destroy()
        except Exception:
            pass

    def Downloading_prosses(self, downloader_obj):
        # start download func
        downloader_obj.download_video()


    def Pause_process(self, downloader_obj):
        # set progress label to current progress
        self.progrss_label.configure(text=f"{downloader_obj.progress:.1f}%")
        
        is_paused = downloader_obj.is_paused

        if is_paused:
            is_paused = False
            self.pause_button.configure(image=self.pause_icon, fg_color="#1F6AA5", hover_color="#1F466D")
        else:
            is_paused = True
            self.pause_button.configure(image=self.continue_icon, fg_color="orange", hover_color = "#CD7F32")

        downloader_obj.is_paused = is_paused


    def update_progress(self, downloader_obj):
        try:
            if not self.download_window or not self.download_window.winfo_exists():
                return

            if downloader_obj.progress == 100:
                self.progrss_label.configure(text="100%")
                self.progress_bar.set(1)
                self.is_downloading = False
                if self.download_window.winfo_exists():
                    self.download_window.destroy()

            else:  
                if downloader_obj.progress is not None:  # check first if there is a value inside progress
                    # set progress label to current progress
                    self.progrss_label.configure(text=f"{downloader_obj.progress:.1f}%")

                    # set the progress bar to a value from 0 to 1
                    bar_value = downloader_obj.progress/100
                    self.progress_bar.set(bar_value)

                    # configure the speed label
                    if downloader_obj.speed is not None:
                        self.speed_label.configure(text=downloader_obj.speed)
                self.is_downloading = True
                self.after(10, self.update_progress, downloader_obj)  # keep updating the progress label every 0.01 seconds
        except Exception as e:
            print(f"Error in update_progress: {e}")

if __name__ == "__main__":
    app = App()
    app.mainloop()