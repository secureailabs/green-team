
import time

from breaker_selenium.common.system_webdriver import SystemWebdriver
from breaker_selenium.common.tab_manager_base import TabManagerBase
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webdriver import WebDriver


class TabManagerTiktok(TabManagerBase):

    def __init__(self, config, webdriver, window_handle):
        super(TabManagerTiktok, self).__init__()
        self.config = config
        self.webdriver = webdriver
        self.window_handle = window_handle
        self.current_url = ''
        self.username_logged_in = None

    def make_active(self):
        if not self.webdriver.current_window_handle == self.window_handle:
            self.webdriver.switch_to.window(str(self.window_handle))
            time.sleep(0.1)

    def action_scrape_user(self, user_handle:str):
        print('action_scrape_user')
        dict_video = self.scrape_dict_video(user_handle)


        for id_video, url_video in dict_video.items():
            self.scrape_video(user_handle, id_video, url_video)

    def scrape_dict_video(self, user_handle:str) -> dict:
        print('scrape_dict_video')
        self.make_active()
        SystemWebdriver.open_url(self.webdriver, f"https://www.tiktok.com/{user_handle}")
        time.sleep(10)
        html = self.webdriver.execute_script("return document.body.innerHTML;")
        with open("full.html","w", encoding="utf-8")  as f:
            f.write(html)
        dict_video = {}
        has_new = True
        while(has_new):
            has_new = self.get_links(user_handle, dict_video)
            self.webdriver.execute_script("window.scrollBy(0,document.body.scrollHeight)", "");
        return dict_video

    def scrape_video(self, user_handle:str,  id_video:str, url_video:str) -> None:
        print('scrape_dict_video')
        print(url_video)
        self.make_active()
        SystemWebdriver.open_url(self.webdriver, url_video)

        time.sleep(4)
        html = self.webdriver.execute_script("return document.body.innerHTML;")
        with open("video.html","w", encoding="utf-8")  as f:
            f.write(html)
        exit(0)

    def get_links(self, user_handle, dict_video):
        has_new = False
        list_element = self.webdriver.find_elements(By.XPATH, "//a[@href]")
        for element in list_element:
            url_video = element.get_attribute("href")
            if f"{user_handle}/video/" in url_video:
                id_video = url_video.split("video/")[-1]
                if id_video not in dict_video:
                    dict_video[id_video] = url_video
                    print(url_video)
                    has_new = True
        return has_new