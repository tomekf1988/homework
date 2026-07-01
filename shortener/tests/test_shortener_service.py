from django.test import TestCase
from django.db import IntegrityError
from unittest.mock import patch


from shortener.models import ShortLink
from shortener.services import ShortenerService
from shortener.exceptions import CodeGenerationError, ShortLinkNotFoundError

class ShortenerServiceTests(TestCase):
    def setUp(self) -> None:
        self.service = ShortenerService()
        self.url = "http://example.com/very-very/long/url/even-longer"

    def test_create_should_create_new_short_link(self) -> None:
        link = self.service.create(self.url)

        self.assertEqual(ShortLink.objects.count(), 1)
        self.assertEqual(link.original_url, self.url)
        self.assertEqual(len(link.code), ShortLink.CODE_LENGTH)

    def test_create_should_return_existing_short_link(self) -> None:
        existing = ShortLink.objects.create(
            original_url=self.url,
            code="abc123"
        )

        link = self.service.create(self.url)

        self.assertEqual(ShortLink.objects.count(), 1)
        self.assertEqual(link, existing)

    def test_resolve_should_return_short_link(self) -> None:
        code = "abc123"
        existing = ShortLink.objects.create(
            original_url=self.url,
            code=code,
        )

        resolved = self.service.resolve(code)

        self.assertEqual(existing, resolved)

    def test_resolve_should_raise_when_code_does_not_exist(self) -> None:
        with self.assertRaises(ShortLinkNotFoundError):
            self.service.resolve("unknown")

    @patch("shortener.services.ShortLink.objects.create")
    def test_create_should_retry_when_code_collision_occurs(
        self,
        create_mock,
    ) -> None:
        created = ShortLink(
            original_url=self.url,
            code="xyz789",
        )

        create_mock.side_effect = [
            IntegrityError(),
            created,
        ]

        result = self.service.create(self.url)

        self.assertEqual(result, created)
        self.assertEqual(create_mock.call_count, 2)

    @patch("shortener.services.ShortLink.objects.create")
    def test_create_should_raise_when_max_attempts_are_exceeded(
        self,
        create_mock,
    ) -> None:
        create_mock.side_effect = IntegrityError()

        with self.assertRaises(CodeGenerationError):
            self.service.create(self.url)

        self.assertEqual(create_mock.call_count, self.service.MAX_ATTEMPTS)


