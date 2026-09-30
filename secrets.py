import keyring
from keyring.errors import PasswordDeleteError
SERVICE_NAME = "OCLI"
ACCOUNT_NAME = "api_key"


def save_api_key(api_key):
    keyring.set_password(SERVICE_NAME, ACCOUNT_NAME, api_key)


def load_api_key():
    return keyring.get_password(SERVICE_NAME, ACCOUNT_NAME)

def delete_api_key():
    try:
        keyring.delete_password(
            SERVICE_NAME,
            ACCOUNT_NAME,
        )
        return True

    except keyring.errors.PasswordDeleteError:
        return False