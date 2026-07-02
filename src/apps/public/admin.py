from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from apps.public.models import AboutUsModel, ArticleModel, BannerModel


@admin.register(BannerModel)
class BannerAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "ordering",
        "is_active",
        "created_at",
    )

    list_display_links = ("id", "title")

    list_filter = ("is_active", "created_at")

    search_fields = ("title", "alt_text")

    readonly_fields = ("created_at", "updated_at")

    fieldsets = (
        (
            _("Banner Information"),
            {
                "fields": (
                    "title",
                    "image",
                    "alt_text",
                    "link",
                    "ordering",
                    "is_active",
                )
            },
        ),
        (_("System Information"), {"fields": ("created_at", "updated_at")}),
    )

    ordering = ("ordering",)
    date_hierarchy = "created_at"


@admin.register(AboutUsModel)
class AboutUsAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "created_at",
    )

    list_display_links = ("id",)

    readonly_fields = ("created_at", "updated_at")

    fieldsets = (
        (_("About Us Content"), {"fields": ("content", "image")}),
        (_("System Information"), {"fields": ("created_at", "updated_at")}),
    )

    ordering = ("-created_at",)
    date_hierarchy = "created_at"


@admin.register(ArticleModel)
class ArticleAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "slug",
        "is_published",
        "created_at",
    )

    list_display_links = ("id", "title")

    list_filter = ("is_published", "created_at")

    search_fields = ("title", "slug", "meta_title", "meta_description")

    readonly_fields = ("created_at", "updated_at", "slug")

    fieldsets = (
        (
            _("Article Information"),
            {
                "fields": (
                    "title",
                    "slug",
                    "image",
                    "content",
                    "is_published",
                )
            },
        ),
        (
            _("SEO Information"),
            {
                "fields": (
                    "meta_title",
                    "meta_description",
                )
            },
        ),
        (_("System Information"), {"fields": ("created_at", "updated_at")}),
    )

    ordering = ("-created_at",)
    date_hierarchy = "created_at"
