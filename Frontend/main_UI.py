# needed libraries
import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, font as tkFont
import time

# local imports
from Backend.mainApp import BackApp

class FrontApp(ctk.CTk):
    def __init__(self, version):
        super().__init__()
        self.create_main_window(version)
        self.create_entry_field()
        self.create_download_button()

        self.backApp = BackApp(frontApp=self)
        self.error_message = None
        self.is_check = False


    def create_main_window(self, version):
        self.title(f"DownTube V{version}")
        self.geometry("500x150")
        self.resizable(False, False)

        # type my name well, i mean i am gonna do that you know (-_-)
        my_name = ctk.CTkLabel(self, text="By/ Ahmed Ibrahim", font=("Arial", 12))
        my_name.place(x=10, y=120)

        # set an icon for the app
        #self.iconbitmap("./Images/DownTube_icon.ico")

    def create_entry_field(self):
        # Link entry
        self.linkEntry = ctk.CTkEntry(self,
                                       width=450,
                                       height=30,
                                       placeholder_text="Enter the video link here...",
                                       corner_radius=5,
                                       font=("Arial", 14),
                                       border_color="#4D4D4D")
        
        self.linkEntry.pack(pady=20)

    def create_download_button(self):
        # start download button
        self.download_button = ctk.CTkButton(self,
                                             text="Download",
                                             width=80,
                                             height=30,
                                             corner_radius=3,
                                             font=("Arial", 14),
                                             command=self.on_download_click)
        
        self.download_button.place(relx=1, rely=1, anchor="center", x=-70, y=-30)

    def on_download_click(self):
        if self.error_message:
            self.error_message.destroy()
        try:
            self.linkEntry.configure(border_color="#4D4D4D")
            link = self.linkEntry.get()
            if not link:
                raise Exception("Please enter a link first.")

            self.backApp.check_existance(url=link)
        except Exception as e:
            self.display_error_message(message=e)

    def display_error_message(self, message):
            self.is_check = False

            self.linkEntry.configure(border_color="red")
            self.error_message = ctk.CTkLabel(master=self, 
                                                       text=message, 
                                                       text_color="red", 
                                                       font=ctk.CTkFont(family="Arial", size=12, weight='bold'))
            self.error_message.place(relx=0, rely=0, x=30, y=52)
    def display_loading_message(self):
        self.loading_dots = " . . ."

        self.loading_message_text = ctk.CTkLabel(master=self, 
                                            text="Looking for the URL"+self.loading_dots, 
                                            text_color="#FFEB38",
                                            font=ctk.CTkFont(family="Arial", size=12, weight='bold'))
        
        self.loading_message_text.place(x=30, y=52)
        
        while self.is_check:
            if self.loading_dots.count(".") >= 3:
                self.loading_dots = ""
            else:
                self.loading_dots+= " ."

            self.after(0, self.loading_message_text.configure(text="Looking for the URL"+self.loading_dots))

            time.sleep(0.5)

        self.loading_message_text.destroy()


    