from rest_framework import serializers

from shortener.models import ShortLink


class CreateShortLinkRequestSerializer(serializers.Serializer):
    original_url = serializers.URLField()


class CreateShortLinkResponseSerializer(serializers.Serializer):
    short_url = serializers.URLField()


class ResolveShortLinkResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShortLink
        fields = ("original_url",)