from context_tiktok import ContextTiktok

context = ContextTiktok("C:\\data\\team-green\\")
type_extract = "summary_chatgpt"
list_handle = ["@katiekickscancer"]
import openai

openai.api_key = "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"
# Set the model and prompt
model_engine = "text-davinci-003"
prompt_base = "Generate a summary for: "
# Generate a summary for: <text>
# Get a list of symptoms from: <text>
# Enumerate a timeline of events from the following text: <text>

# Set the maximum number of tokens to generate in the response
max_tokens = 1024


for user_handle in list_handle:
    video_dict = context.load_video_dict(user_handle)
    for id_video, video in video_dict.items():

        if context.has_transcript(user_handle, id_video):
            if not context.has_extract(user_handle, id_video, type_extract):
                print(id_video)
                text = context.load_transcript(user_handle, id_video)["text"]
                if 3000 < len(text.split(" ")):
                    text = " ".join(text.split(" ")[:2000]) #TODO max text lenght
                prompt = prompt_base + text
                # Generate a response
                completion = openai.Completion.create(
                    engine=model_engine,
                    prompt=prompt,
                    max_tokens=max_tokens,
                    temperature=0.5,
                    top_p=1,
                    frequency_penalty=0,
                    presence_penalty=0
                )
                extract = completion.choices[0].text
                context.save_extract(user_handle, id_video, type_extract, extract)