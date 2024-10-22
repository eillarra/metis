from cryptography.fernet import Fernet
from django.conf import settings
from django.db.models import TextField


def encrypt(text: str) -> str:
    """Encrypt a text.

    :param text: The text to encrypt.
    :returns: The encrypted token.
    """
    fernet = Fernet(settings.ENCRYPTION_KEY)
    return fernet.encrypt(text.encode()).decode()


def decrypt(token: bytes | str, ttl: int | None = None) -> str:
    """Decrypt a token.

    :param token: The token to decrypt.
    :param ttl: The time-to-live of the token.
    :returns: The decrypted text.
    """
    fernet = Fernet(settings.ENCRYPTION_KEY)
    return fernet.decrypt(token, ttl).decode()


class EncryptedTextField(TextField):
    """A Django text field that is encrypted when saved to the database."""

    def from_db_value(self, value: str, expression, connection) -> str:
        """Decrypts the value when retrieved from the database."""
        return decrypt(value)

    def to_python(self, value: str) -> str:
        """Encrypts the value when saved to the database."""
        return encrypt(value)
