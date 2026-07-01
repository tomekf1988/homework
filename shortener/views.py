from django.urls import reverse

from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.views import APIView

from shortener.exceptions import ShortLinkNotFoundError
from shortener.serializers import (
    CreateShortLinkRequestSerializer,
    CreateShortLinkResponseSerializer,
    ResolveShortLinkResponseSerializer,
)
from shortener.services import ShortenerService


class ShortLinkCreateAPIView(APIView):
    def post(self, request: Request) -> Response:
        request_serializer = CreateShortLinkRequestSerializer(
            data=request.data,
        )
        request_serializer.is_valid(raise_exception=True)

        service = ShortenerService()
        short_link = service.create(
            request_serializer.validated_data["original_url"],
        )

        path = reverse(
            "resolve-short-link",
            kwargs={"code": short_link.code},
        )

        response_serializer = CreateShortLinkResponseSerializer(
            {
                "short_url": request.build_absolute_uri(path),
            }
        )

        return Response(
            response_serializer.data,
            status=status.HTTP_201_CREATED,
        )


class ShortLinkResolveAPIView(APIView):
    def get(self, request: Request, code: str) -> Response:
        service = ShortenerService()

        try:
            short_link = service.resolve(code)
        except ShortLinkNotFoundError as exc:
            raise NotFound("Short link not found.") from exc

        response_serializer = ResolveShortLinkResponseSerializer(
            short_link,
        )

        return Response(response_serializer.data)