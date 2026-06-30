from django.db import models


class Contact(models.Model):
    username = models.CharField(max_length=100, verbose_name='Имя')
    phone = models.CharField(max_length=17, blank=True, null=False, verbose_name='Телефон')
    email = models.EmailField(verbose_name='Email')
    message = models.TextField(verbose_name='Сообщение')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата отправки')

    def __str__(self):
        return f'{self.username} ({self.email})'

    class Meta:
        verbose_name = 'Контакт'
        verbose_name_plural = 'Контакты'
        ordering = ['-created_at']
