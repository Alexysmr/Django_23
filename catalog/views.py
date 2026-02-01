from django.shortcuts import render
from django.http import HttpResponse

from catalog.models import Product, Contact


def index(request) -> HttpResponse:
    """Отработка и рендеринг запроса GET главной страницы"""
    last_products = Product.objects.order_by('-created_at')[:5]
    print("Последние 5 продуктов:", list(last_products.values('id', 'name', 'created_at')))
    context = {
        'last_products': last_products,
    }
    return render(request, 'catalog/index.html', context=context)


def contacts(request) -> HttpResponse:
    """Отработка и рендеринг запросов GET и POST страницы контактов"""
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        print(f'You have new message from {name}({phone}): {message}')
        Contact.objects.create(name=name, email=phone, message=message)
        html_answer = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Сообщение отправлено</title>
            <link rel="stylesheet" href="/static/bootstrap.min.css">
        </head>
        <body>
            <div class="container mt-4">
                <a href="/" class="btn btn-primary">Каталог</a>
                <a href="/contacts/" class="btn btn-primary">Контакты</a>
                <h3>Спасибо, {name.name()}! Ваше сообщение \"{message}\" получено.</h3>
            </div>
        </body>
        </html>
        """
        return HttpResponse(html_answer)
    contacts_list = Contact.objects.all().order_by('-created_at')
    context = {'contacts': contacts_list}
    return render(request, 'catalog/contacts.html', context)
