# needed libraries
import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, font as tkFont

# local imports
from Backend.mainApp import BackApp

class FrontApp(ctk.CTk):
    def __init__(self, version):
        super().__init__()
        self.create_main_window(version)
        self.create_entry_field()
        self.create_download_button()

        self.backApp = BackApp()


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
                                       font=("Arial", 14))
        
        self.linkEntry.pack(pady=20)

        self.create_past_button()

    def create_past_button(self):
        #create a button on top of the entry field that get the copied link
        past_button = ctk.CTkButton(master=self.linkEntry, width=40, height=20, text="Past")
        past_button.place(relx=1, rely=0.5, anchor="center", x=-25)

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
        try:
            link = self.linkEntry.get()
            if not link:
                raise Exception("Please enter a link first.")

            self.backApp.check_existance()
        except Exception as e:
            print(e)