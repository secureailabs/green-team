from context_tiktok import ContextTiktok
from transformers import pipeline

context = ContextTiktok("C:\\data\\team-green\\")
type_extract = "summary_distilbart"
list_handle = ["@katiekickscancer"]
summarizer = pipeline("summarization")
for user_handle in list_handle:
    video_dict = context.load_video_dict(user_handle)
    for id_video, video in video_dict.items():

        if context.has_transcript(user_handle, id_video):
            if not context.has_extract(user_handle, id_video, type_extract):
                print(id_video)
                to_tokenize = context.load_transcript(user_handle, id_video)["text"]
                summarized = summarizer(to_tokenize, min_length=75, max_length=300)
                context.save_extract(user_handle, id_video, type_extract, summarized[0]["summary_text"])