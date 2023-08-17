import os
from queue import Queue

from ffmpeg_transcoder import FFmpegTranscoder
from job_worker import JobWorker
from patient_story_prompter import PatientStoryPrompter
from whisper_transcriber import WhisperTranscriber
from youtube_downloader import YoutubeDownloader

if __name__ == "__main__":
    path_dir_data = os.environ.get("PATH_DIR_DATA_PATIENT_STORY")
    dict_job = {}
    url_queue = Queue()
    worker = JobWorker(path_dir_data, url_queue, dict_job)
    downloader = YoutubeDownloader()
    transcoder = FFmpegTranscoder()
    transcriber = WhisperTranscriber()
    prompter = PatientStoryPrompter()

    url = "https://www.youtube.com/watch?v=kn5PT3mAOHQ"
    job_id = worker.get_job_id(url)
    path_file_video = os.path.abspath(f"data/video/{job_id}/video.mp4")
    path_file_audio = os.path.abspath(f"data/audio/{job_id}/audio.mp3")
    path_file_transcript = os.path.abspath(f"data/transcript/{job_id}/transcript.json")
    path_file_story = os.path.abspath(f"data/story/{job_id}/story.json")

    # downloader.download(url, path_file_video)
    # transcoder.extract_audio(path_file_video, path_file_audio)
    # transcriber.transcribe(path_file_audio, path_file_transcript)
    prompter.prompt(path_file_transcript, path_file_story)
