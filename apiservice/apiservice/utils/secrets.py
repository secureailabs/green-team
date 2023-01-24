from typing import Dict

secrets: Dict[str, str] = {
    "jwt_secret": "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7",
    "refresh_secret": "52bb444a1aabb9a76792527e6605349e1cbc7fafb8624de4e0ddde4f84ad4066",
    "password_pepper": "06ac6368872b368a8c67e41c1a8faa46e8471818cdbb442345fbb2205b9fc225",
}


def get_secret(secret_name: str) -> str:
    """Get the value of a secret

    :param secret_name: key for the value to be fetched
    :type secret_name: str
    :return: the value for the key if it exists or an exception
    :rtype: str
    """
    global secrets

    if secret_name not in secrets:
        raise Exception(f"Secret {secret_name} not found")

    return secrets[secret_name]
