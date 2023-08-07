import hashlib
import json
import os
import threading
from queue import Queue

from ffmpeg_transcoder import FFmpegTranscoder
from patient_story_prompter import PatientStoryPrompter
from whisper_transcriber import WhisperTranscriber
from youtube_downloader import YoutubeDownloader


class JobWorker(threading.Thread):
    def __init__(self, path_dir_data: str, queue: Queue, dict_job: dict):
        super().__init__()
        self.path_dir_data = path_dir_data
        self.queue = queue
        self.dict_job = dict_job
        self.downloader = YoutubeDownloader()
        self.transcoder = FFmpegTranscoder()
        self.transcriber = WhisperTranscriber()
        self.prompter = PatientStoryPrompter()

    def get_job_id(self, url: str) -> str:
        return hashlib.sha256(url.encode()).hexdigest()

    def process_queue(self):
        job_id = self.queue.get()
        job = self.dict_job[job_id]
        self.process_job(job)

    def process_job(self, job: dict):
        job_id = job["job_id"]
        url = job["url"]
        path_file_video = os.path.abspath(os.path.join(self.path_dir_data, "video", job_id, "video.mp4"))
        path_file_audio = os.path.abspath(os.path.join(self.path_dir_data, "audio", job_id, "audio.mp3"))

        path_file_transcript = os.path.abspath(
            os.path.join(self.path_dir_data, "transcript", job_id, "transcript.json")
        )
        path_file_story = os.path.abspath(os.path.join(self.path_dir_data, "story", job_id, "y.json"))
        try:

            self.downloader.download(url, path_file_video)
            self.transcoder.extract_audio(path_file_video, path_file_audio)
            self.transcriber.transcribe(path_file_audio, path_file_transcript)
            self.prompter.prompt(path_file_transcript, path_file_story)
            with open(path_file_story, "r") as file:
                job["story"] = json.load(file)
            job["status"] = "completed"
        except Exception as e:
            job["status"] = "failed"
            job["error_message"] = str(e)

    def run(self):
        while True:
            self.process_queue()
