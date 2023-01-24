from typing import Dict

secrets: Dict[str, str] = {}


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
