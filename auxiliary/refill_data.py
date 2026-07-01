import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'site_22.settings')
django.setup()

from catalog.models import Category, Product

# Перезаполненеие БД неросредственно из данного файла через удаление данных из БД

Category.objects.all().delete()
Product.objects.all().delete()

cat1 = Category.objects.create(name='Электроника', description='Гаджеты и устройства')
cat2 = Category.objects.create(name='Книги', description='Художественная и техническая литература')
cat3 = Category.objects.create(name='Одежда', description='Мужская и женская одежда')
cat4 = Category.objects.create(name='ЭМИ', description='Электро-музыкальные инструменты')

Product.objects.create(
    name='Ноутбук Lenovo',
    description='Мощный ноутбук для работы и игр',
    category=cat1,
    price=52000.00
)
Product.objects.create(
    name='Смартфон Samsung',
    description='Современный смартфон с хорошей камерой',
    category=cat1,
    price=32000.00
)
Product.objects.create(
    name='Python для начинающих',
    description='Книга по основам Python',
    category=cat2,
    price=1500.00
)
Product.objects.create(
    name='Электрогитара',
    description='Электрогитара 6-ти струнная, H-H, тремоло Floyd Rose, Volume, Tone',
    category=cat4,
    price=15000.00
)
Product.objects.create(
    name='Wah-wah педаль',
    description='Педаль эффектов Wah-wah, VOX модель V847A "Cry baby"',
    category=cat4,
    price=8000.00
)


print('Данные созданы заново')
