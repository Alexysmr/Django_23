from django.core.management.base import BaseCommand
from django.core.management import call_command


class Command(BaseCommand):
    help = 'Удаляет все данные из БД и загружает фикстуры'

    def handle(self, *args, **options):
        """Перезаполнение БД из фикстур через удаление данных из БД"""
        self.stdout.write('Удаляем данные из БД.')
        from catalog.models import Category, Product
        Product.objects.all().delete()
        Category.objects.all().delete()

        self.stdout.write('Загружаем фикстуры...')
        call_command('loaddata', 'category_test_data.json', app_label='catalog')
        call_command('loaddata', 'product_test_data.json', app_label='catalog')

        self.stdout.write(self.style.SUCCESS('Заполнение БД выполнено успешно!'))
