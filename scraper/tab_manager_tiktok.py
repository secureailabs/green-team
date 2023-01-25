
import time

from breaker_selenium.common.system_webdriver import SystemWebdriver
from breaker_selenium.common.tab_manager_base import TabManagerBase
from bs4 import BeautifulSoup
from context_tiktok import ContextTiktok
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

    def action_scrape_user(self, context:ContextTiktok, user_handle:str):
        print('action_scrape_user')
        dict_video = self.scrape_dict_video(context, user_handle)
        for id_video, video in dict_video.items():
            self.action_scrape_video_html(context, user_handle, id_video, video)
            context.save_video_dict(user_handle, dict_video)


    #scrape video dict
    def scrape_dict_video(self, context:ContextTiktok, user_handle:str) -> dict:
        print('scrape_dict_video')
        if not context.has_user_html(user_handle):
            self.make_active()
            SystemWebdriver.open_url(self.webdriver, f"https://www.tiktok.com/{user_handle}")
            time.sleep(10)
            dict_video = {}
            has_new = True
            user_html:str = ""
            while(has_new):
                user_html = self.webdriver.execute_script("return document.body.innerHTML;")
                has_new = self.get_video_links(user_handle, dict_video, user_html)
                self.webdriver.execute_script("window.scrollBy(0,document.body.scrollHeight)", "");
            context.save_user_html(user_handle, user_html)

        dict_video = {}
        user_html =  context.load_user_html(user_handle)
        self.get_video_links(user_handle, dict_video, user_html)
        return dict_video



    def get_video_links(self, user_handle:str, dict_video:dict, html:str):
        has_new = False
        soup = BeautifulSoup(html, features="html5lib")
        for element in soup.find_all('a', href=True):
            url_video_page = element['href']
            if f"{user_handle}/video/" in url_video_page:
                id_video = url_video_page.split("video/")[-1]
                if id_video not in dict_video:
                    dict_video[id_video] = {"url_video_page":url_video_page}
                    print(url_video_page)
                    has_new = True
        return has_new

    #scrape video
    def action_scrape_video_html(self, context:ContextTiktok, user_handle:str,  id_video:str, video:dict) -> None:
        print('action_scrape_video')
        if not context.has_video_html(user_handle, id_video):
            url_video_page = video["url_video_page"]
            print(url_video_page)
            self.make_active()
            SystemWebdriver.open_url(self.webdriver, url_video_page)

            time.sleep(4)
            video_html = self.webdriver.execute_script("return document.body.innerHTML;")
            context.save_video_html(user_handle, id_video, video_html)
        video_html = context.load_video_html(user_handle, id_video)
        soup = BeautifulSoup(video_html, features="html5lib")

        for element in soup.find_all('video'):
            url_video_content = element['src'].split("?")[0]

            video["url_video_content"] = url_video_content
            if "prime" in url_video_content:
                video["is_private"] = True
            else:
                video["is_private"] = False