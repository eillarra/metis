from cryptography.fernet import Fernet
from django.conf import settings
from django.db.models import TextField


def encrypt(text: str) -> str:
    """Encrypts a text.

    Args:
        text: The text to encrypt.

    Returns:
        The encrypted token.
    """
    fernet = Fernet(settings.ENCRYPTION_KEY)
    return fernet.encrypt(text.encode()).decode()


def decrypt(token: bytes | str, ttl: int | None = None) -> str:
    """Decrypts a token.

    Args:
        token: The token to decrypt.
        ttl: The time-to-live of the token.

    Returns:
        The decrypted text.
    """
    fernet = Fernet(settings.ENCRYPTION_KEY)
    return fernet.decrypt(token, ttl).decode()


class EncryptedTextField(TextField):
    """A Django text field that is encrypted when saved to the database."""

    def from_db_value(self, value: str, expression, connection):
        """Decrypts the value when retrieved from the database."""
        return decrypt(value)

    def to_python(self, value: str):
        """Encrypts the value when saved to the database."""
        return encrypt(value)
