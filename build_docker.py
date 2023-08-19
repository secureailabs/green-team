import os
import re
import subprocess


def build_docker(image_name: str, image_tag: str):
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


if __name__ == "__main__":

    with open("app/__init__.py") as file:
        version_module = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', file.read(), re.MULTILINE).group(1)  # type: ignore
    with open("app/__init__.py") as file:
        title = re.search(r'^__title__\s*=\s*[\'"]([^\'"]*)[\'"]', file.read(), re.MULTILINE).group(1)  # type: ignore
    image_name = f"arin/{title}-image"
    image_tag = version_module
    conainer_name = f"{title}-container"
    print(image_tag)
    build_docker(image_name, image_tag)
