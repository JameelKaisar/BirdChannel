from django.db import models

from django.core.exceptions import ValidationError
from django.utils.text import slugify
from django.conf import settings
from os.path import splitext

# Create your models here.

class ConservationCategory(models.Model):
    def user_directory_path(instance, filename):
        return f"conservation/{slugify(instance.category_slug)}/{instance.category_slug}.{filename.split('.')[-1]}"

    conservation_category = models.CharField(max_length=100)
    category_summary = models.CharField(max_length=500)
    category_slug = models.SlugField(max_length=100)

    category_image = models.FileField(upload_to=user_directory_path)

    class Meta:
        verbose_name_plural = "Conservation Categories"

    def validate_unique(self, *args, **kwargs):
        self.category_slug = slugify(self.conservation_category)
        super(ConservationCategory, self).validate_unique(*args, **kwargs)
        if self.__class__.objects.filter(category_slug=self.category_slug).exists():
            raise ValidationError(message=f"Category with name \"{self.conservation_category}\" already exists.", code='unique_together',)

    def delete(self, *args, **kwargs):
        if self.category_image:
            self.category_image.storage.delete(self.category_image.name)
        super(ConservationCategory, self).delete(*args, **kwargs)

    def __str__(self):
        return self.conservation_category

class ConservationContent(models.Model):
    def user_directory_path(instance, filename):
        return f"conservation/{instance.content_category.category_slug}/{slugify(instance.conservation_content)}.{filename.split('.')[-1]}"

    conservation_content = models.CharField(max_length=100)
    content_text = models.TextField()
    content_time = models.DateTimeField(auto_now_add=True)
    content_file = models.FileField(upload_to=user_directory_path, blank=True, null=True)

    content_user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name="User", on_delete=models.CASCADE)
    content_category = models.ForeignKey(ConservationCategory, verbose_name="Category", on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Conservation Content"

    def file_type(self):
        name, extension = splitext(self.content_file.name.lower())
        if extension in ['.apng', '.avif', '.gif', '.jpg', '.jpeg', '.jfif', '.pjpeg', '.pjp', '.png', '.svg', '.webp']:
            return 'image'
        elif extension in ['.mp4', 'webm']:
            return 'video'
        elif extension in ['.mp3', '.wav', '.ogg', '.m4a']:
            return 'audio'
        else:
            return 'file'

    def delete(self, *args, **kwargs):
        if self.content_file:
            self.content_file.storage.delete(self.content_file.name)
        super(ConservationContent, self).delete(*args, **kwargs)

    def __str__(self):
        return self.conservation_content

class BirdingCategory(models.Model):
    def user_directory_path(instance, filename):
        return f"birding/{slugify(instance.category_slug)}/{instance.category_slug}.{filename.split('.')[-1]}"

    birding_category = models.CharField(max_length=100)
    category_summary = models.CharField(max_length=500)
    category_slug = models.SlugField(max_length=100)

    category_image = models.FileField(upload_to=user_directory_path)

    class Meta:
        verbose_name_plural = "Birding Categories"

    def validate_unique(self, *args, **kwargs):
        self.category_slug = slugify(self.birding_category)
        super(BirdingCategory, self).validate_unique(*args, **kwargs)
        if self.__class__.objects.filter(category_slug=self.category_slug).exists():
            raise ValidationError(message=f"Category with name \"{self.birding_category}\" already exists.", code='unique_together',)

    def delete(self, *args, **kwargs):
        if self.category_image:
            self.category_image.storage.delete(self.category_image.name)
        super(BirdingCategory, self).delete(*args, **kwargs)

    def __str__(self):
        return self.birding_category

class BirdingContent(models.Model):
    def user_directory_path(instance, filename):
        return f"birding/{instance.content_category.category_slug}/{slugify(instance.birding_content)}.{filename.split('.')[-1]}"

    birding_content = models.CharField(max_length=100)
    content_text = models.TextField()
    content_time = models.DateTimeField(auto_now_add=True)
    content_file = models.FileField(upload_to=user_directory_path, blank=True, null=True)

    content_user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name="User", on_delete=models.CASCADE)
    content_category = models.ForeignKey(BirdingCategory, verbose_name="Category", on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Birding Content"

    def file_type(self):
        name, extension = splitext(self.content_file.name.lower())
        if extension in ['.apng', '.avif', '.gif', '.jpg', '.jpeg', '.jfif', '.pjpeg', '.pjp', '.png', '.svg', '.webp']:
            return 'image'
        elif extension in ['.mp4', 'webm']:
            return 'video'
        elif extension in ['.mp3', '.wav', '.ogg', '.m4a']:
            return 'audio'
        else:
            return 'file'

    def delete(self, *args, **kwargs):
        if self.content_file:
            self.content_file.storage.delete(self.content_file.name)
        super(BirdingContent, self).delete(*args, **kwargs)

    def __str__(self):
        return self.birding_content
