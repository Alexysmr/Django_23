from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404
from django.core.paginator import Paginator

from catalog.models import Product, Contact, Category
from .forms import ProductForm


def index(request) -> HttpResponse:
    """Отработка и рендеринг запроса GET главной страницы с отображением списка продуктов"""
    all_products = Product.objects.all()
    paginator = Paginator(all_products, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
    }
    return render(request, 'catalog/index.html', context)


def contacts(request) -> HttpResponse:
    """Отработка и рендеринг запросов GET и POST страницы контактов"""
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        message = request.POST.get('message')
        print(f'You have new message from {name}({phone}, {email}): {message}')
        Contact.objects.create(name=name, phone=phone, email=email, message=message)
        request.session['last_submission'] = {
            'name': name,
            'message': message
        }
        return redirect('contact_success')
    contacts_list = Contact.objects.all().order_by('-created_at')
    context = {'contacts': contacts_list}
    return render(request, 'catalog/contacts.html', context)


def contact_success(request) -> HttpResponse:
    context = request.session.get('last_submission', {})
    return render(request, 'catalog/answer_by_message.html', context)


def added_products(request) -> HttpResponse:
    """Последние 5 внесённых в БД продуктов"""
    last_products = Product.objects.order_by('-created_at')[:5]
    print("Последние 5 продуктов:", list(last_products.values('id', 'name', 'created_at')))
    context = {
        'last_products': last_products,
    }
    return render(request, 'catalog/added_products.html', context)


def product_details(request, pk) -> HttpResponse:
    try:
        product = get_object_or_404(Product, id=pk)
        context = {
            'product': product,
        }
        return render(request, 'catalog/product_details.html', context)
    except Http404:
        # Кастомная обработка именно для товаров
        context = {
            'error_title': 'Товар не найден',
            'error_message': f'Скорее всего товара с номером {pk} не существует.',
        }
        return render(request, 'catalog/404.html', context, status=404)


def products_by_category(request, category_id):
    """Отображает товары только из указанной категории"""
    category = get_object_or_404(Category, id=category_id)
    products = Product.objects.filter(category=category)

    context = {
        'category': category,
        'products': products,
    }
    return render(request, 'catalog/products_by_category.html', context)


def add_product(request):
    """Добавление товаров пользователем"""
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('added_products')
    else:
        form = ProductForm()

    context = {'form': form}
    return render(request, 'catalog/add_product.html', context)
