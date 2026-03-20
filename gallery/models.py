from django.db import models
import os


class Section(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)
    cover_image = models.ImageField(upload_to='covers/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', 'created_at']

    def __str__(self):
        return self.name

    def media_count(self):
        return self.media.count()

    def image_count(self):
        return self.media.filter(media_type='image').count()

    def video_count(self):
        return self.media.filter(media_type='video').count()

    def get_cover(self):
        if self.cover_image:
            url = self.cover_image.url
            if 'image/upload' in url:
                # Sections covers are always images, but just in case
                return url
            return url
        first_image = self.media.filter(media_type='image').first()
        if first_image:
            return first_image.get_url
        return None


class MediaItem(models.Model):
    MEDIA_TYPES = [('image', 'Image'), ('video', 'Video')]
    section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name='media')
    file = models.FileField(upload_to='uploads/')
    media_type = models.CharField(max_length=10, choices=MEDIA_TYPES)
    caption = models.CharField(max_length=255, blank=True)
    order = models.PositiveIntegerField(default=0)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', '-uploaded_at']

    @property
    def get_url(self):
        if not self.file:
            return ""
        url = self.file.url
        if self.media_type == 'video' and 'image/upload' in url:
            return url.replace('image/upload', 'video/upload')
        return url

    def __str__(self):
        return f"{self.media_type} - {self.caption or self.file.name}"

    def filename(self):
        return os.path.basename(self.file.name)

    def extension(self):
        return os.path.splitext(self.file.name)[1].lower()
