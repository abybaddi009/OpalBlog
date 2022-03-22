from django.db import models
from django.contrib.auth import get_user_model
from django.dispatch import receiver
from django.shortcuts import reverse
from django.utils import timezone

from django.core.exceptions import ValidationError
from django.db.models.signals import pre_save, post_save
from django.utils.translation import gettext_lazy as _

from .utlis import slugify


User = get_user_model()


def validate_title(value):
    if len(value) <= 10:
        raise ValidationError(
            _("%(value)s must be larger than 10 characters"),
            params={"value": value},
        )


class Blog(models.Model):
    title = models.CharField(
        verbose_name="Blog Title", max_length=256, validators=[validate_title]
    )
    description = models.TextField(blank=True)

    slug = models.SlugField(max_length=64, unique=True, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name="blogs")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("blog:blog-detail", args=[self.slug])


class Post(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.PROTECT, related_name="posts")

    title = models.CharField(
        verbose_name="Post Title", max_length=256, validators=[validate_title]
    )
    content = models.TextField(blank=True)

    slug = models.SlugField(max_length=64, editable=False, null=True, blank=True)

    created_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name="posts")
    created_at = models.DateTimeField(auto_now_add=True)

    modified_at = models.DateTimeField(auto_now=True)

    published = models.BooleanField(verbose_name="Is Published", default=False)
    published_at = models.DateTimeField(
        verbose_name="Published at", null=True, blank=True
    )

    @property
    def author(self):
        return self.created_by

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("blog:post-detail", args=[self.slug])


@receiver(pre_save, sender=Blog)
def blog_pre_save(sender, instance, *args, **kwargs):
    instance.slug = slugify(sender, instance.title)


@receiver(pre_save, sender=Post)
def post_pre_save(sender, instance, *args, **kwargs):
    # slugify the title
    instance.slug = slugify(sender, instance.title)


@receiver(post_save, sender=Post)
def post_post_save(sender, instance, created, *args, **kwargs):
    # If published and no publication time, set to now
    if instance.published and not instance.published_at:
        instance.published_at = timezone.now()
