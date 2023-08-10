import json
import os
from queue import Queue

from fastapi import FastAPI, HTTPException
from job_worker import JobWorker

app = FastAPI()

path_dir_data = os.environ.get("PATH_DIR_DATA_PATIENT_STORY")
dict_job = {}
url_queue = Queue()
worker = JobWorker(path_dir_data, url_queue, dict_job)
worker.start()


@app.post("/process_youtube/")
async def process_youtube(url: str):
    job_id = worker.get_job_id(url)
    # TODO check url is youtube url

    job = {"job_id": job_id, "url": url, "status": "queued", "error_message": "", "story": ""}
    dict_job[job_id] = job
    url_queue.put(job_id)
    return job


@app.get("/job/{job_id}")
async def get_job(job_id: str):
    if job_id not in dict_job:
        raise HTTPException(status_code=404, detail="Job not found")
    return dict_job[job_id]


@app.get("/transcript/{job_id}")
async def get_transcript(job_id: str):
    if job_id not in dict_job:
        raise HTTPException(status_code=404, detail="Job not found")
    job = dict_job[job_id]
    if job["status"] != "completed":
        raise HTTPException(status_code=404, detail="Job not finished")
    path_file_transcript = os.path.abspath(os.path.join(path_dir_data, "transcript", job_id, "transcript.json"))
    with open(path_file_transcript, "r") as file:
        transcript = json.load(file)
    return transcript


@app.get("/story/{job_id}")
async def get_story(job_id: str):
    if job_id not in dict_job:
        raise HTTPException(status_code=404, detail="Job not found")
    job = dict_job[job_id]
    if job["status"] != "completed":
        raise HTTPException(status_code=404, detail="Job not finished")
    path_file_story = os.path.abspath(os.path.join(path_dir_data, "story", job_id, "story.json"))
    with open(path_file_story, "r") as file:
        story = json.load(file)
    return story


@app.get("/redo_prompt/{job_id}")
async def get_story(job_id: str):
    if job_id not in dict_job:
        raise HTTPException(status_code=404, detail="Job not found")
    job = dict_job[job_id]
    if job["status"] != "completed":
        raise HTTPException(status_code=404, detail="Job not finished")
    path_file_transcript = os.path.abspath(os.path.join(path_dir_data, "transcript", job_id, "transcript.json"))
    path_file_story = os.path.abspath(os.path.join(path_dir_data, "story", job_id, "story.json"))
    worker.prompter.prompt(path_file_transcript, path_file_story)
    with open(path_file_story, "r") as file:
        story = json.load(file)
    return story


@app.get("/joblist/")
async def get_joblist():
    return {"joblist": list(dict_job.values())}
