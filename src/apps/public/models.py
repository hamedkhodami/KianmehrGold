from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models
from django.utils.translation import gettext_lazy as _
from slugify import slugify

from apps.core.models import BaseModel


class BannerModel(BaseModel):
    title = models.CharField(_("Title"), max_length=255, blank=True, null=True)

    image = models.ImageField(_("Image"), upload_to="public/banners")

    alt_text = models.CharField(_("Alt Text"), max_length=255, blank=True, null=True)

    link = models.URLField(_("Link"), blank=True, null=True)

    ordering = models.PositiveIntegerField(_("Ordering"), default=0)

    is_active = models.BooleanField(_("Active"), default=True)

    class Meta:
        verbose_name = _("Banner")
        verbose_name_plural = _("Banners")
        ordering = ["ordering"]

    def __str__(self):
        return self.title or f"Banner {self.id}"


class AboutUsModel(BaseModel):
    content = models.TextField(_("Content"))
    image = models.ImageField(
        _("Image"), upload_to="public/about", blank=True, null=True
    )

    class Meta:
        verbose_name = _("About Us")
        verbose_name_plural = _("About Us")


class ArticleModel(BaseModel):
    title = models.CharField(_("Title"), max_length=255)
    slug = models.SlugField(_("Slug"), unique=True)

    image = models.ImageField(
        _("Image"), upload_to="public/articles", blank=True, null=True
    )

    content = RichTextUploadingField(_("Content"))

    meta_title = models.CharField(
        _("Meta Title"), max_length=255, blank=True, null=True
    )
    meta_description = models.CharField(
        _("Meta Description"), max_length=500, blank=True, null=True
    )

    is_published = models.BooleanField(_("Published"), default=True)

    class Meta:
        verbose_name = _("Article")
        verbose_name_plural = _("Articles")

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title, separator="-", allow_unicode=True)
            slug = base_slug
            counter = 1

            while ArticleModel.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1

            self.slug = slug

        super().save(*args, **kwargs)
