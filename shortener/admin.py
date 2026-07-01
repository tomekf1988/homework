from django.contrib import admin

from shortener.models import ShortLink


@admin.register(ShortLink)
class ShortLinkAdmin(admin.ModelAdmin):
    list_display = (
        "code",
        "original_url",
        "created_at",
    )
    search_fields = (
        "code",
        "original_url",
    )
    ordering = ("-created_at",)