import requests
from context_tiktok import ContextTiktok

context = ContextTiktok("C:\\data\\team-green\\")

list_handle = ["@aprilgrierson2", "@katiekickscancer"]
for user_handle in list_handle:
    print(user_handle)
    video_dict = context.load_video_dict(user_handle)
    for id_video, video in video_dict.items():

        print(id_video)
        if video["is_private"]:
            print("private")
            continue
        if context.has_video_content(user_handle, id_video):
            print("present")
            continue
        url_video_content = video["url_video_content"]
        response = requests.get(url_video_content)
        if response.status_code == 200:
            context.save_video_content(user_handle, id_video, response.content)
        else:
            print(id_video)
            print(url_video_content)
            print(response.status_code)
            print(response.content)
            raise Exception("not 200")


