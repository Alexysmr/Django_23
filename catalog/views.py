from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import Http404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView,TemplateView, RedirectView
from django.views.generic.edit import FormView
from django.urls import reverse_lazy

from auxiliary.utils import user_in_groups
from auxiliary.constants import CATALOG_GROUP_LIST
from .models import Product, Contact, Category
from .forms import ProductForm, ContactForm


class CustomPermissionMixin(PermissionRequiredMixin):
    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return super().handle_no_permission()
        messages.error(self.request, "Для совершения данного действия требуются права администратора")
        return redirect('catalog:index')


class IndexView(ListView):
    model = Product
    template_name = 'catalog/index.html'
    context_object_name = 'products'
    paginate_by = 3

    def get_queryset(self):
        # Метод можно не добавлять, но в случае возникновения необходимости предварительной обработки пригодится
        return Product.objects.all().order_by('created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_moderator_products'] = user_in_groups(self.request.user, CATALOG_GROUP_LIST)
        return context


class ContactsView(FormView):
    template_name = 'catalog/contacts.html'
    form_class = ContactForm
    success_url = reverse_lazy('catalog:contact_success')

    def get_context_data(self, **kwargs):
        """Добавление списка контактов в контекст"""
        context = super().get_context_data(**kwargs)
        context['contacts'] = Contact.objects.all().order_by('-created_at')
        return context

    def form_valid(self, form):
        """Обработка валидной формы"""
        contact = form.save()
        self.request.session['last_submission'] = {
            'username': contact.username,
            'message': contact.message,
        }
        print(f'You have new message from {contact.username}({contact.phone}, {contact.email}): {contact.message}')
        return super().form_valid(form)


class ContactSuccessView(TemplateView):
    template_name = 'catalog/answer_by_message.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        last_submission = self.request.session.get('last_submission', {})
        context['username'] = last_submission.get('username', '')
        context['message'] = last_submission.get('message', '')
        return context


class AddedProductsView(LoginRequiredMixin, ListView):
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
                'error_title': 'Ошибка запрашиваемой страницы',
                'error_message': f'Скорее всего того, что Вы задали в адресной строке, на этом сайте не существует.',
            }
            return render(request, 'catalog/404_custom.html', context, status=404)


class ProductEditView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_update.html'
    context_object_name = 'product'

    def get_success_url(self):
        return reverse_lazy('catalog:product_details', kwargs={'pk': self.object.pk})

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.owner != request.user and not request.user.has_perm('catalog.change_product'):
            messages.error(request, "Редактировать можно только свои продукты.")
            return redirect('catalog:product_details', pk=obj.pk)
        return super().dispatch(request, *args, **kwargs)


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
                'error_title': 'Ошибка запрашиваемой страницы',
                'error_message': f'Скорее всего того, что Вы задали в адресной строке, на этом сайте не существует.',
            }
            return render(request, 'catalog/404_custom.html', context, status=404)

    def get_queryset(self):
        return Product.objects.filter(category=self.category)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        return context


class AddProductView(LoginRequiredMixin, CustomPermissionMixin, CreateView):
    form_class = ProductForm
    template_name = 'catalog/add_product.html'
    permission_required = 'catalog.add_product'
    success_url = reverse_lazy('catalog:added_products')

    def form_valid(self, form):
        product = form.save(commit=False)
        product.owner = self.request.user
        product.save()
        return super().form_valid(form)


class DeleteProductView(LoginRequiredMixin, CustomPermissionMixin, DeleteView):
    model = Product
    template_name = 'catalog/product_delete.html'
    context_object_name = 'product'
    permission_required = 'catalog.delete_product'
    success_url = reverse_lazy('catalog:index')

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.owner != request.user and not request.user.has_perm('catalog.delete_product'):
            messages.error(request, "Удалять продукты могут только владелец или модератор.")
            return redirect('catalog:product_details', pk=obj.pk)
        return super().dispatch(request, *args, **kwargs)


class CustomLoginView(LoginView):
    template_name = 'registration/login.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['next'] = self.request.GET.get('next', '')
        return context