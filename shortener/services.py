import logging

from django.db import IntegrityError

from shortener.code_generator import generate_code
from shortener.models import ShortLink
from shortener.exceptions import CodeGenerationError, ShortLinkNotFoundError


logger = logging.getLogger(__name__)


class ShortenerService:
    MAX_ATTEMPTS: int = 10

    def create(self, original_url: str) -> ShortLink:
        try:
            return ShortLink.objects.get(original_url=original_url)
        except ShortLink.DoesNotExist:
            for _ in range(self.MAX_ATTEMPTS):
                try:
                    return ShortLink.objects.create(
                        original_url=original_url,
                        code=generate_code()
                    )
                except IntegrityError:
                    logger.debug("Collision detected")
                    continue
        raise CodeGenerationError()


    def resolve(self, code: str) -> ShortLink:
        try:
            return ShortLink.objects.get(code=code)
        except ShortLink.DoesNotExist as exc:
            raise ShortLinkNotFoundError() from exc

    
