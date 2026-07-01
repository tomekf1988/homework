from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase
from shortener.models import ShortLink

class ShortLinkApiTests(APITestCase):
    def setUp(self) -> None:
        self.url = "http://example.com/very-very/long/url/even-longer"

    def test_should_create_and_resolve_short_link(self) -> None:
        create_response = self.client.post(
            reverse("create-short-link"),
            {
                "original_url": self.url,
            },
            format="json",
        )

        self.assertEqual(
            create_response.status_code,
            status.HTTP_201_CREATED,
        )

        short_url = create_response.data["short_url"]
        code = short_url.rstrip("/").split("/")[-1]

        resolve_response = self.client.get(
            reverse(
                "resolve-short-link",
                kwargs={"code": code},
            )
        )

        self.assertEqual(
            resolve_response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            resolve_response.data["original_url"],
            self.url,
        )
        
    def test_should_return_existing_short_link_for_same_url(self) -> None:
        first_response = self.client.post(
            reverse("create-short-link"),
            {
                "original_url": self.url,
            },
            format="json",
        )

        second_response = self.client.post(
            reverse("create-short-link"),
            {
                "original_url": self.url,
            },
            format="json",
        )

        self.assertEqual(
            first_response.status_code,
            status.HTTP_201_CREATED,
        )

        self.assertEqual(
            second_response.status_code,
            status.HTTP_201_CREATED,
        )

        self.assertEqual(
            first_response.data["short_url"],
            second_response.data["short_url"],
        )

        self.assertEqual(
            ShortLink.objects.count(),
            1,
        )

    def test_should_return_400_for_invalid_url(self) -> None:
        response = self.client.post(
            reverse("create-short-link"),
            {
                "original_url": "not-a-valid-url",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

    def test_should_return_404_for_unknown_short_code(self) -> None:
        response = self.client.get(
            reverse(
                "resolve-short-link",
                kwargs={"code": "unknown"},
            )
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND,
        )

        self.assertEqual(
            response.data["detail"],
            "Short link not found.",
        )