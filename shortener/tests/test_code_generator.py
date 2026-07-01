from django.test import SimpleTestCase

from shortener.code_generator import generate_code
from shortener.models import ShortLink


class GenerateCodeTests(SimpleTestCase):
    def test_should_generate_code_with_expected_length(self) -> None:
        code = generate_code()

        self.assertEqual(len(code), ShortLink.CODE_LENGTH)

    def test_should_generate_only_alphanumeric_characters(self) -> None:
        code = generate_code()

        self.assertTrue(code.isalnum())

    def test_should_generate_different_codes(self) -> None:
        first = generate_code()
        second = generate_code()

        self.assertNotEqual(first, second)