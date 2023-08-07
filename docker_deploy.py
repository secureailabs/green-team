import os
import subprocess

dict_build_args = {}
dict_build_args["ARIN_PYPI_REPOSITORY_URL"] = os.environ.get("ARIN_PYPI_REPOSITORY_URL")
dict_build_args["ARIN_PYPI_USERNAME"] = os.environ.get("ARIN_PYPI_USERNAME")
dict_build_args["ARIN_PYPI_PASSWORD"] = os.environ.get("ARIN_PYPI_PASSWORD")


build_command = "docker build -t arin-patient-story-image"
for key, value in dict_build_args.items():
    build_command += " --build-arg " + key + "=" + value
build_command += " ."
print(build_command)
subprocess.call(build_command, shell=True)
