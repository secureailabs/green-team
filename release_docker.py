# function to tag and push the input image to the docker hub
import os
import subprocess

from deploy_docker import docker_build


def push_image_to_registry(image_name: str, image_tag: str):
    # check docker installed
    DOCKER_REGISTRY_NAME = os.environ["DOCKER_REGISTRY_NAME"]
    AZURE_CLIENT_ID = os.environ["AZURE_CLIENT_ID"]
    AZURE_CLIENT_SECRET = os.environ["AZURE_CLIENT_SECRET"]
    AZURE_TENANT_ID = os.environ["AZURE_TENANT_ID"]
    AZURE_SUBSCRIPTION_ID = os.environ["AZURE_SUBSCRIPTION_ID"]
    image_name_tag = f"{image_name}:{image_tag}"

    # echo "login to azure account"
    command = f"az login --service-principal --username {AZURE_CLIENT_ID} --password {AZURE_CLIENT_SECRET} --tenant {AZURE_TENANT_ID}"
    print(command)
    subprocess.run(command, shell=True)
    command = f"az account set --subscription {AZURE_SUBSCRIPTION_ID}"
    print(command)
    subprocess.run(command, shell=True)

    command = f"az acr login --name {DOCKER_REGISTRY_NAME}"
    print(command)
    subprocess.run(command, shell=True)

    command = f"docker tag {image_name_tag} {DOCKER_REGISTRY_NAME}.azurecr.io/{image_name_tag}"
    subprocess.run(command, shell=True)
    print(command)

    command = f"docker push {DOCKER_REGISTRY_NAME}.azurecr.io/{image_name_tag}"
    print(command)
    subprocess.run(command, shell=True)


if __name__ == "__main__":
    project_name = "arin-patient-story"
    image_name = f"arin/{project_name}-image"
    image_tag = "0.2.0"
    conainer_name = f"{project_name}-container"
    docker_build(image_name, image_tag)
    push_image_to_registry(image_name, image_tag)
