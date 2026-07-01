from django.urls import path

from shortener.views import (
    ShortLinkCreateAPIView,
    ShortLinkResolveAPIView,
)

urlpatterns = [
    path(
        "short-links/",
        ShortLinkCreateAPIView.as_view(),
        name="create-short-link",
    ),
    path(
        "shrt/<str:code>/",
        ShortLinkResolveAPIView.as_view(),
        name="resolve-short-link",
    ),
]