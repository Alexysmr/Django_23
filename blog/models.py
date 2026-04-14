from django.db import models
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill


class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    preview = models.ImageField(upload_to='blog', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    published = models.BooleanField(default=False)
    number_of_views = models.IntegerField(default=0)
    image_thumbnail = ImageSpecField(
        source='preview',
        processors=[ResizeToFill(300, 300)],
        format='JPEG',
        options={'quality': 85}
    )

    def __str__(self):
        return f'{self.title} - {self.number_of_views}'

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'
