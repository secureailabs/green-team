from time import sleep

import requests

if __name__ == "__main__":
    url_base = "http://localhost:8000/"
    response = requests.post(url_base + "process_youtube/?url=https%3A%2F%2Fwww.youtube.com%2Fwatch%3Fv%3DBvVzcobqjck")
    job = response.json()
    job_id = job["job_id"]
    while job["status"] != "completed":
        print(job["status"])
        job = requests.get(url_base + f"job/{job_id}").json()
        sleep(1)

    transcript = requests.get(url_base + f"transcript/{job_id}").json()
    print(transcript["text"])
    story = requests.get(url_base + f"story/{job_id}").json()
    print(story)
