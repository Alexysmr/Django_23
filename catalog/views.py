from django.db import models
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import Http404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.core.cache import cache
from django.urls import reverse_lazy

from auxiliary.utils import user_in_groups
from auxiliary.constants import (CATALOG_GROUP_LIST, CACHE_KEY_PRODUCT_LIST_MODERATOR,
                                 CACHE_KEY_PRODUCT_LIST_OWNER, CACHE_KEY_PRODUCT_LIST_PUBLIC)
from .models import Product, Category
from .forms import ProductForm
from .services import get_products_by_category


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
        user = self.request.user

        if user.groups.filter(name='Модератор продуктов').exists() or user.is_superuser:
            cached_ids = cache.get(CACHE_KEY_PRODUCT_LIST_MODERATOR)
            if cached_ids is not None:
                products = Product.objects.filter(id__in=cached_ids)
                order = {id: i for i, id in enumerate(cached_ids)}
                return sorted(products, key=lambda p: order.get(p.id, 0))
            queryset = Product.objects.all().order_by('created_at')
            ids = list(queryset.values_list('id', flat=True))
            cache.set(CACHE_KEY_PRODUCT_LIST_MODERATOR, ids, 60 * 15)
            return queryset

        if user.is_authenticated:
            cache_key = f"{CACHE_KEY_PRODUCT_LIST_OWNER}_{user.id}"
            cached_ids = cache.get(cache_key)
            if cached_ids is not None:
                products = Product.objects.filter(id__in=cached_ids)
                order = {id: i for i, id in enumerate(cached_ids)}
                return sorted(products, key=lambda p: order.get(p.id, 0))
            queryset = Product.objects.filter(
                models.Q(owner=user) | models.Q(is_published=True)
            ).order_by('created_at')
            ids = list(queryset.values_list('id', flat=True))
            cache.set(cache_key, ids, 60 * 15)
            return queryset

        cached_ids = cache.get(CACHE_KEY_PRODUCT_LIST_PUBLIC)
        if cached_ids is not None:
            products = Product.objects.filter(id__in=cached_ids)
            order = {id: i for i, id in enumerate(cached_ids)}
            return sorted(products, key=lambda p: order.get(p.id, 0))
        queryset = Product.objects.filter(is_published=True).order_by('created_at')
        ids = list(queryset.values_list('id', flat=True))
        cache.set(CACHE_KEY_PRODUCT_LIST_PUBLIC, ids, 60 * 15)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_moderator_products'] = user_in_groups(self.request.user, CATALOG_GROUP_LIST)
        context['is_catalog_home'] = not self.request.GET.get('page') or self.request.GET.get('page') == '1'
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
                'error_message': f'Вероятно того, что Вы задали в адресной строке, на этом сайте не существует.',
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

    def form_valid(self, form):
        response = super().form_valid(form)
        cache.delete(f'product_detail_{self.object.id}')
        return response

class ProductsByCategoryView(ListView):
    model = Product
    template_name = 'catalog/products_by_category.html'
    context_object_name = 'products'

    def get(self, request, *args, **kwargs):
        """Ловим 404 на уровне GET, как в ProductDetailView"""

        category_id = kwargs['category_id']
        products = get_products_by_category(category_id)
        if products is None:
            context = {
                'error_title': 'Ошибка запрашиваемой страницы',
                'error_message': f'Скорее всего того, что Вы задали в адресной строке, на этом сайте не существует.',
            }
            return render(request, 'catalog/404_custom.html', context, status=404)
        self.category = Category.objects.get(id=category_id)
        self.products = products
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        return self.products

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

    def form_valid(self, form):
        response = super().form_valid(form)
        cache.delete(f'product_detail_{self.object.id}')
        return response

class CustomLoginView(LoginView):
    template_name = 'registration/login.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['next'] = self.request.GET.get('next', '')
        return context
