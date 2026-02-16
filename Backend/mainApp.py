import time
from threading import Thread

class BackApp():
    def __init__(self, frontApp):
        self.frontApp = frontApp


    def check_existance(self, url):
        get_info_thread = Thread(target=self.get_video_info, args=(url,), daemon=True)
        get_info_thread.start()

        self.frontApp.display_loading_message()

    def get_video_info(self, url):
        print(f"Start looking for {url}")
        self.frontApp.is_check = True
        time.sleep(5)
        print("done")
        self.frontApp.is_check = False