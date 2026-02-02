from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='products', blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.name} - {self.price} руб., {self.category}'

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'

class Contact(models.Model):
    name = models.CharField(max_length=100, verbose_name='Имя')
    email = models.EmailField(verbose_name='Email')
    message = models.TextField(verbose_name='Сообщение')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата отправки')

    def __str__(self):
        return f'{self.name} ({self.email})'

    class Meta:
        verbose_name = 'Контакт'
        verbose_name_plural = 'Контакты'
        ordering = ['-created_at']
