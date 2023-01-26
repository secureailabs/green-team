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
