import secrets
import string

from shortener.models import ShortLink


ALPHABET = string.ascii_letters + string.digits

def generate_code(length: int = ShortLink.CODE_LENGTH) -> str:
    return "".join(
        secrets.choice(ALPHABET)
        for _ in range(length)
    )