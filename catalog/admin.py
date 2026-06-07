from django.contrib import admin
from catalog.models import Category, Product, Contact


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


@admin.action(description='Снять с публикации', permissions=['can_unpublish_product'])
def make_unpublished(modeladmin, request, queryset):
    queryset.update(is_published=False)
    modeladmin.message_user(request, 'Выбранные продукты сняты с публикации.')

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'category', 'is_published')
    list_filter = ('category', 'is_published')
    search_fields = ('name', 'description')
    actions = [make_unpublished]

    def has_can_unpublish_product_permission(self, request):
        return request.user.has_perm('catalog.can_unpublish_product')


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'created_at')
    search_fields = ('username', 'email')
