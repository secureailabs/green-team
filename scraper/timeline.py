import json
from datetime import datetime

from context_tiktok import ContextTiktok

dict_timestamp = {}
dict_timestamp["Js27JwrXsIg"] = 1672057462
dict_timestamp["92Da-XC-7dk"] = 1669465462
dict_timestamp["xu6uv0aGTCY"] = 1668601462
dict_timestamp["jT2PFFmeeBk"] = 1648297462
dict_timestamp["HOpILlb9FyM"] = 1647433462
dict_timestamp["JcLkww0tEIc"] = 1645878262
dict_timestamp["ZW2-ciZbXtM"] = 1645446262
dict_timestamp["Iue_GsVen0U"] = 1645014262
dict_timestamp["BvVzcobqjck"] = 1644063862


def get_timestamp(context:ContextTiktok, user_handle:str, id_video:str) -> int:
    if id_video in dict_timestamp:
        return dict_timestamp[id_video]
    html = context.load_video_html(user_handle, id_video)

    list_split = html.split("createTime")
    for split in list_split:
        if split[:3] == '":"':
            return int(split[3:13])
    return 0

context = ContextTiktok("C:\\data\\team-green\\")

list_handle = ["@katiekickscancer"]

for user_handle in list_handle:
    dict_timeline ={}
    dict_timeline["user_handle"] = user_handle
    dict_timeline["timeline"] = []

    video_dict = context.load_video_dict(user_handle)
    for id_video, video in video_dict.items():
        if context.has_video_content(user_handle, id_video):
            if not context.has_transcript(user_handle, id_video):
                raise Exception("processing incomplete")
            if not context.has_extract(user_handle, id_video, "summary_chatgpt"):
                raise Exception("processing incomplete")
            transcript = context.load_transcript(user_handle, id_video)
            summary = context.load_extract(user_handle, id_video, "summary_chatgpt")
            symptoms = context.has_extract(user_handle, id_video, "symptoms_chatgpt")
            path_file_video = context._path_video_content(user_handle, id_video)
            timestamp = get_timestamp(context, user_handle, id_video)
            datestring = str(datetime.fromtimestamp(timestamp))

            timeline_item = {}
            timeline_item["_id"] =id_video
            timeline_item["user_id"] = user_handle
            timeline_item["video_path"] = path_file_video
            if "url_video_content" in video:
                timeline_item["video_content_url"] = video["url_video_content"]
            else:
                timeline_item["video_content_url"] = ""
            timeline_item["video_page_url"] = video["url_video_page"]
            timeline_item["timestamp"] = timestamp
            timeline_item["datestring"] = datestring
            timeline_item["text"] = transcript["text"]
            timeline_item["summary"] = summary
            timeline_item["symptoms"] = symptoms
            timeline_item["title"] = summary.split(".")[0]
            dict_timeline["timeline"].append(timeline_item)
    with open("timeline.json", "w") as file:
        json.dump(dict_timeline, file)


