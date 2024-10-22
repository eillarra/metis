from unittest.mock import patch

import pytest
from cryptography.fernet import Fernet

from metis.utils.cryptography import EncryptedTextField


@pytest.mark.parametrize(
    "text",
    [
        "Hello, World!",
        "Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
        "👋🌍",
        "Μητις",
    ],
)
@pytest.mark.unit
def test_encrypt_decrypt(text):
    """Test that the encryption functions work, via EncryptedTextField."""
    field = EncryptedTextField()

    with patch("metis.utils.cryptography.settings.ENCRYPTION_KEY", Fernet.generate_key()):
        db_value = field.get_prep_value(text)
        assert db_value != text  # The value should be encrypted

        python_value = field.from_db_value(db_value, None, None)  # type: ignore
        assert python_value == text  # The value should be decrypted back to the original
