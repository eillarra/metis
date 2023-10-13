from cryptography.fernet import Fernet
from django.conf import settings
from django.db.models import TextField
from typing import Union


def encrypt(text: str) -> str:
    """
    Encrypts a token.
    """

    fernet = Fernet(settings.ENCRYPTION_KEY)
    return fernet.encrypt(text.encode()).decode()


def decrypt(token: Union[bytes, str], ttl: int | None = None) -> str:
    """
    Decrypts a token.
    """

    fernet = Fernet(settings.ENCRYPTION_KEY)
    return fernet.decrypt(token, ttl).decode()


class EncryptedTextField(TextField):
    """
    A text field that is encrypted when saved to the database.
    """

    def from_db_value(self, value: str, expression, connection):
        if value is not None:
            return decrypt(value)
        return value

    def to_python(self, value: str):
        if value is not None:
            return encrypt(value)
        return value
