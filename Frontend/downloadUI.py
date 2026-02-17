import customtkinter as ctk

class Down_UI(ctk.CTkToplevel):
    def __init__(self, master):
        super().__init__()
        self.create_child_window(master)


    def create_child_window(self, master):
        self.master = master
        self.geometry("720x360")
        self.title("Download Options")
        self.resizable(False, False)
        self.focus_set()
        self.grab_set()

        # create a frame to hold title and thumbnail
        top_frame = ctk.CTkFrame(self, width=700, height=200, fg_color="#1A1A1A", corner_radius=3)
        top_frame.pack(pady=10)