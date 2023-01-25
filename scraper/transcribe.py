import json

import whisper
from context_tiktok import ContextTiktok

context = ContextTiktok("C:\\data\\team-green\\")

model = whisper.load_model("base")
list_handle = ["@katiekickscancer"]

for user_handle in list_handle:
    dict_timeline ={}
    dict_timeline["user_handle"] = user_handle
    dict_timeline["timeline"] = []

    video_dict = context.load_video_dict(user_handle)
    for id_video, video in video_dict.items():
        if context.has_video_content(user_handle, id_video):
            if not context.has_transcript(user_handle, id_video):
                print(id_video, flush=True)
                path_file_video = context._path_video_content(user_handle, id_video)
                transcript = model.transcribe(path_file_video)
                context.save_transcript(user_handle, id_video, transcript)
            transcript = context.load_transcript(user_handle, id_video)
            path_file_video = context._path_video_content(user_handle, id_video)
            timeline_item = {}
            timeline_item["_id"] =id_video
            timeline_item["user_id"] = user_handle
            timeline_item["video_path"] = path_file_video
            timeline_item["video_content_url"] = video["url_video_content"]
            timeline_item["video_page_url"] = video["url_video_page"]
            timeline_item["timestamp"] = id_video
            timeline_item["text"] = transcript["text"]
            timeline_item["summary"] = transcript["text"]
            timeline_item["title"] = transcript["text"][:100]
            dict_timeline["timeline"].append(timeline_item)
    with open("timeline.json", "w") as file:
        json.dump(dict_timeline, file)
