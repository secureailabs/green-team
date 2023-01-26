import os
from typing import Dict, Optional

from context_tiktok import ContextTiktok
from pytube import Channel, Playlist, YouTube


class UserChannel(Playlist):

    def __init__(self, user_handle: str, proxies: Optional[Dict[str, str]] = None):
        """Construct a :class:`Channel <Channel>`.
        :param str url:
            A valid YouTube channel URL.
        :param proxies:
            (Optional) A dictionary of proxies to use for web requests.
        """
        self.user_handle = user_handle
        self.channel_url = (
            f"https://www.youtube.com/{self.user_handle}"
        )
        super().__init__(self.channel_url, proxies)


        self.videos_url = self.channel_url + '/videos'
        self.playlists_url = self.channel_url + '/playlists'
        self.community_url = self.channel_url + '/community'
        self.featured_channels_url = self.channel_url + '/channels'
        self.about_url = self.channel_url + '/about'

        # Possible future additions
        self._playlists_html = None
        self._community_html = None
        self._featured_channels_html = None
        self._about_html = None


def download(video_page_url):
    youtube_object = YouTube(video_page_url)
    youtube_object = youtube_object.streams.get_highest_resolution()
    try:
        youtube_object.download()
    except:
        print("An error has occurred")
    print("Download is completed successfully")


#channel = Channel('https://www.youtube.com/c/ProgrammingKnowledge')
#channel = Channel('https://www.youtube.com/channel/UCcf5yVgHvI8-__g0RHjfrTw')
channel = UserChannel('@katiekickscancer4840')
# #https://www.youtube.com/@katiekickscancer4840/videos
# list_video_page_url = []
# for video_page_url in list_video_page_url
# download(video_page_url)


# print(len(channel.videos))
# for video in channel.videos:
#     print(video)
#     video.streams.first().download()

context = ContextTiktok("C:\\data\\team-green\\")
user_handle = "@katiekickscancer"
list_url_video = [
"https://www.youtube.com/watch?v=Js27JwrXsIg",
"https://www.youtube.com/watch?v=92Da-XC-7dk",
"https://www.youtube.com/watch?v=xu6uv0aGTCY",
"https://www.youtube.com/watch?v=jT2PFFmeeBk",
"https://www.youtube.com/watch?v=HOpILlb9FyM",
"https://www.youtube.com/watch?v=JcLkww0tEIc",
"https://www.youtube.com/watch?v=ZW2-ciZbXtM",
"https://www.youtube.com/watch?v=Iue_GsVen0U",
"https://www.youtube.com/watch?v=BvVzcobqjck"]
video_dict = context.load_video_dict(user_handle)
for id_video, video in video_dict.items():
    video["video_source"] = "tiktok"
    video["id_video"] = id_video

for url in list_url_video:
    id_video = url.split("https://www.youtube.com/watch?v=")[1]
    print(id_video)
    video = {}
    video["video_source"] = "youtube"
    video["id_video"] = id_video
    video["url_video_page"] = url
    video_dict[id_video] = video
    youtube = YouTube(url)
    if context.has_video_content(user_handle, id_video):
        continue
    output_path = os.path.dirname(context._path_video_content(user_handle, id_video))
    filename = id_video + ".mp4"
    youtube.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().last().download(output_path, filename)

context.save_video_dict(user_handle, video_dict)