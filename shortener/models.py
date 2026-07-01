from django.db import models

class ShortLink(models.Model):
    CODE_LENGTH = 8

    original_url = models.URLField(unique=True)
    code = models.CharField(
        max_length=CODE_LENGTH,
        unique=True,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.code