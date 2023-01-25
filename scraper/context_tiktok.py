import json
import os


class ContextTiktok:

    def __init__(self, path_root) -> None:
        self.__path_root = path_root

    #user html
    def _path_user_html(self, user_handle:str) -> str:
        path_dir =os.path.join(self.__path_root, user_handle, "user_html")
        if not os.path.isdir(path_dir):
            os.makedirs(path_dir)
        return os.path.join(path_dir, "dom.hmtl")

    def has_user_html(self, user_handle:str) -> bool:
        return os.path.isfile(self._path_user_html(user_handle))

    def save_user_html(self, user_handle:str, user_html:str) -> None:
        with open(self._path_user_html(user_handle), "w", encoding="utf-8") as file:
            file.write(user_html)

    def load_user_html(self, user_handle:str) -> str:
        with open(self._path_user_html(user_handle), "r", encoding="utf-8") as file:
            return file.read()


    #video dict
    def _path_video_dict(self, user_handle:str) -> str:
        path_dir = os.path.join(self.__path_root, user_handle)
        if not os.path.isdir(path_dir):
            os.makedirs(path_dir)
        return os.path.join(path_dir, "video_dict.json")

    def has_video_dict(self, user_handle:str) -> bool:
        return os.path.isfile(self._path_video_dict(user_handle))

    def save_video_dict(self, user_handle:str, video_dict:dict) -> None:
        with open(self._path_video_dict(user_handle), "w", encoding="utf-8") as file:
            json.dump(video_dict, file)

    def load_video_dict(self, user_handle:str) -> dict:
        with open(self._path_video_dict(user_handle), "r", encoding="utf-8") as file:
            return json.load(file)

    #video html
    def _path_video_html(self, user_handle:str, id_video:str) -> str:
        path_dir = os.path.join(self.__path_root, user_handle, "video_html")
        if not os.path.isdir(path_dir):
            os.makedirs(path_dir)
        return os.path.join(path_dir, id_video + ".hmtl")

    def has_video_html(self, user_handle:str, id_video:str) -> bool:
        return os.path.isfile(self._path_video_html(user_handle, id_video))

    def save_video_html(self, user_handle:str, id_video:str, video_html:str) -> None:
        with open(self._path_video_html(user_handle, id_video), "w", encoding="utf-8") as file:
            file.write(video_html)

    def load_video_html(self, user_handle:str, id_video:str) -> str:
        with open(self._path_video_html(user_handle, id_video), "r", encoding="utf-8") as file:
            return file.read()

    #video content
    def _path_video_content(self, user_handle:str, id_video:str) -> str:
        path_dir = os.path.join(self.__path_root, user_handle, "video_content")
        if not os.path.isdir(path_dir):
            os.makedirs(path_dir)
        return os.path.join(path_dir, id_video + ".mp4")

    def has_video_content(self, user_handle:str, id_video:str) -> bool:
        return os.path.isfile(self._path_video_content(user_handle, id_video))

    def save_video_content(self, user_handle:str, id_video:str, video_html:bytes) -> None:
        with open(self._path_video_content(user_handle, id_video), "wb") as file:
            file.write(video_html)

    def load_video_content(self, user_handle:str, id_video:str) -> bytes:
        with open(self._path_video_content(user_handle, id_video), "rb") as file:
            return file.read()

    #transcript
    def _path_transcript(self, user_handle:str, id_video:str) -> str:
        path_dir = os.path.join(self.__path_root, user_handle, "transcript")
        if not os.path.isdir(path_dir):
            os.makedirs(path_dir)
        return os.path.join(path_dir, id_video + ".mp4")

    def has_transcript(self, user_handle:str, id_video:str) -> bool:
        return os.path.isfile(self._path_transcript(user_handle, id_video))

    def save_transcript(self, user_handle:str, id_video:str, transcript:dict) -> None:
        with open(self._path_transcript(user_handle, id_video), "w") as file:
            json.dump(transcript, file)

    def load_transcript(self, user_handle:str, id_video:str) -> dict:
        with open(self._path_transcript(user_handle, id_video), "r") as file:
            return json.load(file)


    # summary
    def _path_summary(self, user_handle:str, id_video:str) -> str:
        path_dir = os.path.join(self.__path_root, user_handle, "transcript")
        if not os.path.isdir(path_dir):
            os.makedirs(path_dir)
        return os.path.join(path_dir, id_video + ".mp4")

    def has_summary(self, user_handle:str, id_video:str) -> bool:
        return os.path.isfile(self._path_summary(user_handle, id_video))

    def save_summary(self, user_handle:str, id_video:str, video_html:str) -> None:
        with open(self._path_summary(user_handle, id_video), "w") as file:
            file.write(video_html)

    def load_summary(self, user_handle:str, id_video:str) -> str:
        with open(self._path_summary(user_handle, id_video), "r") as file:
            return file.read()
