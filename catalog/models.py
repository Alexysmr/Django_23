from django.db import models
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill
from django.conf import settings


class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='catalog/', blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='products')
    is_published = models.BooleanField(default=False, verbose_name='Опубликован')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image_thumbnail = ImageSpecField(
        source='image',
        processors=[ResizeToFill(300, 300)],
        format='JPEG',
        options={'quality': 85}
    )

    def __str__(self):
        return f'{self.name} - {self.price} руб., {self.category}'

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'
        permissions = [
            ('can_unpublish_product', 'can_unpublish_product'),
        ]
