from django.shortcuts import render, get_object_or_404
from django.http import Http404
from django.views.generic import ListView, DetailView, CreateView
from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from catalog.models import Product, Contact, Category
from .forms import ProductForm, ContactForm


class IndexView(ListView):
    model = Product
    template_name = 'catalog/index.html'
    context_object_name = 'products'
    paginate_by = 3

    def get_queryset(self):
        # Метод можно не добавлять, но в случае возникновения необходимости предварительной обработки пригодится
        return Product.objects.all().order_by('created_at')


class ContactsView(FormView):
    template_name = 'catalog/contacts.html'
    form_class = ContactForm
    success_url = reverse_lazy('contact_success')

    def get_context_data(self, **kwargs):
        """Добавление списка контактов в контекст"""
        context = super().get_context_data(**kwargs)
        context['contacts'] = Contact.objects.all().order_by('-created_at')
        return context

    def form_valid(self, form):
        """Обработка валидной формы"""
        contact = form.save()
        self.request.session['last_submission'] = {
            'name': contact.name,
            'message': contact.message,
        }
        print(f'You have new message from {contact.name}({contact.phone}, {contact.email}): {contact.message}')
        return super().form_valid(form)


class AddedProductsView(ListView):
    model = Product
    template_name = 'catalog/added_products.html'
    context_object_name = 'last_products'

    def get_queryset(self):
        return Product.objects.order_by('-created_at')[:5]


class ProductDetailView(DetailView):
    """Визуализация подробностей товара с кастомной обработкой 404"""
    model = Product
    template_name = 'catalog/product_details.html'
    context_object_name = 'product'

    def get(self, request, *args, **kwargs):
        """Обработка GET-запроса и возможной ошибки 404"""
        try:
            self.object = self.get_object()
            context = self.get_context_data(object=self.object)
            return self.render_to_response(context)
        except Http404:
            context = {
                'error_title': 'Товар не найден',
                'error_message': f'Скорее всего товара с номером {kwargs.get("pk")} не существует.',
            }
            return render(request, 'catalog/404_custom.html', context, status=404)


class ProductsByCategoryView(ListView):
    model = Product
    template_name = 'catalog/products_by_category.html'
    context_object_name = 'products'

    def get(self, request, *args, **kwargs):
        """Ловим 404 на уровне GET, как в ProductDetailView"""
        try:
            self.category = get_object_or_404(Category, id=kwargs['category_id'])
            return super().get(request, *args, **kwargs)
        except Http404:
            context = {
                'error_title': 'Категория не найдена',
                'error_message': f'Категории с номером {kwargs.get("category_id")} не существует.',
            }
            return render(request, 'catalog/404_custom.html', context, status=404)

    def get_queryset(self):
        return Product.objects.filter(category=self.category)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        return context


class AddProductView(CreateView):
    form_class = ProductForm
    template_name = 'catalog/add_product.html'
    success_url = reverse_lazy('added_products')
