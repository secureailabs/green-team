import os
import subprocess

dict_build_args = {}
dict_build_args["ARIN_PYPI_REPOSITORY_URL"] = os.environ.get("ARIN_PYPI_REPOSITORY_URL")
dict_build_args["ARIN_PYPI_USERNAME"] = os.environ.get("ARIN_PYPI_USERNAME")
dict_build_args["ARIN_PYPI_PASSWORD"] = os.environ.get("ARIN_PYPI_PASSWORD")


image_name = "arin-patient-story-image"
conainer_name = "arin-patient-story-conatianer"

build_command = f"docker build -t {image_name}"
for key, value in dict_build_args.items():
    build_command += f" --build-arg {key}={value}"
build_command += " ."
print(build_command)
subprocess.call(build_command, shell=True)

subprocess.call(f"docker stop {conainer_name}", shell=True)
subprocess.call(f"docker rm {conainer_name}", shell=True)

dict_start_args = {}
dict_start_args["PATH_DIR_DATA_PATIENT_STORY"] = "/data/patient_story"
dict_start_args["PATH_FILE_FFMPEG"] = "/usr/bin/ffmpeg"
dict_mount_args = {}
start_command = f"docker run -d --name {conainer_name}"
for key, value in dict_start_args.items():
    start_command += f" -e {key}={value}"
start_command += f" -p 8000:8000 {image_name}"
print(start_command)
subprocess.call(start_command, shell=True)
