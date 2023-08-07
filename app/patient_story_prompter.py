import json
import os


class PatientStoryPrompter:
    def __init__(self):
        pass

    def prompt(self, path_file_transcript: str, path_file_story: str):
        if not os.path.isfile(path_file_transcript):
            raise RuntimeError("audio file does not exist")
        path_dir_story = os.path.dirname(path_file_story)
        if not os.path.exists(path_dir_story):
            os.makedirs(path_dir_story)

        with open(path_file_transcript, "r") as file:
            transcript = json.load(file)

        print(transcript["text"])

        story = {}  # TODO
        with open(path_file_story, "w") as file:
            json.dump(story, file)
