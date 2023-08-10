import os
import re
import subprocess


def docker_build(image_name: str, image_tag: str):
    image_name_tag = f"{image_name}:{image_tag}"
    dict_build_args = {}
    dict_build_args["ARIN_PYPI_REPOSITORY_URL"] = os.environ.get("ARIN_PYPI_REPOSITORY_URL")
    dict_build_args["ARIN_PYPI_USERNAME"] = os.environ.get("ARIN_PYPI_USERNAME")
    dict_build_args["ARIN_PYPI_PASSWORD"] = os.environ.get("ARIN_PYPI_PASSWORD")

    build_command = f"docker build -t {image_name_tag}"
    build_command += " --progress=plain"
    for key, value in dict_build_args.items():
        build_command += f" --build-arg {key}={value}"
    build_command += " ."
    print(build_command)
    subprocess.call(build_command, shell=True)


def docker_start(image_name: str, image_version: str, conainer_name: str):
    image_name_tag = f"{image_name}:{image_tag}"
    subprocess.call(f"docker stop {conainer_name}", shell=True)
    subprocess.call(f"docker rm {conainer_name}", shell=True)

    dict_environ = {}
    dict_environ["PATH_DIR_DATA_PATIENT_STORY"] = "/data/patient_story"
    dict_environ["PATH_FILE_FFMPEG"] = "/usr/bin/ffmpeg"
    dict_environ["OPENAI_API_KEY"] = os.environ.get("OPENAI_API_KEY")
    dict_mount = {}
    start_command = f"docker run -d --name {conainer_name}"
    for key, value in dict_environ.items():
        start_command += f" -e {key}={value}"
    start_command += f" -p 8000:8000 {image_name_tag}"
    print(start_command)
    subprocess.call(start_command, shell=True)


if __name__ == "__main__":

    with open("app/__init__.py") as file:
        version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', file.read(), re.MULTILINE).group(1)  # type: ignore
    with open("app/__init__.py") as file:
        title = re.search(r'^__title__\s*=\s*[\'"]([^\'"]*)[\'"]', file.read(), re.MULTILINE).group(1)  # type: ignore
    image_name = f"arin/{title}-image"
    image_tag = "0.1.0"
    conainer_name = f"{title}-container"

    docker_build(image_name, image_tag)
    docker_start(image_name, image_tag, conainer_name)
    docker_start(image_name, image_tag, conainer_name)
