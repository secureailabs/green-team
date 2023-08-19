import os
import re
import subprocess


def start_docker(image_name: str, image_tag: str, conainer_name: str):
    image_name_tag = f"{image_name}:{image_tag}"
    subprocess.call(f"docker stop {conainer_name}", shell=True)
    subprocess.call(f"docker rm {conainer_name}", shell=True)

    dict_environ = {}
    dict_environ["PATH_DIR_DATA_PATIENT_STORY"] = "/data/patient_story"
    dict_environ["PATH_DIR_PROMPT_CACHE"] = "/data/prompt_cache"

    dict_environ["PATH_FILE_FFMPEG"] = "/usr/bin/ffmpeg"
    dict_environ["OPENAI_ENGINE_NAME"] = "gpt-4"
    dict_environ["OPENAI_API_KEY"] = os.environ.get("OPENAI_API_KEY")
    dict_environ["AZURE_DATASET_CONNECTIONSTRING"] = os.environ.get("AZURE_DATASET_CONNECTIONSTRING")
    dict_environ["AZURE_PROMPT_CONTAINER_NAME"] = os.environ.get("AZURE_PROMPT_CONTAINER_NAME")

    dict_mount = {}
    start_command = f"docker run -d --name {conainer_name}"
    for key, value in dict_environ.items():
        start_command += f" -e {key}={value}"
    start_command += f" -p 8000:8000 {image_name_tag}"
    print(start_command)
    subprocess.call(start_command, shell=True)


if __name__ == "__main__":

    with open("app/__init__.py") as file:
        version_module = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', file.read(), re.MULTILINE).group(1)  # type: ignore
    with open("app/__init__.py") as file:
        title = re.search(r'^__title__\s*=\s*[\'"]([^\'"]*)[\'"]', file.read(), re.MULTILINE).group(1)  # type: ignore
    image_name = f"arin/{title}-image"
    image_tag = version_module
    conainer_name = f"{title}-container"
    start_docker(image_name, image_tag, conainer_name)
