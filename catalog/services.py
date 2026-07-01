from .models import Product, Category

def get_products_by_category(category_id):
    """
    Возвращает список продуктов для указанной категории.
    При отсутствии категории — возвращает None.
    """
    try:
        category = Category.objects.get(id=category_id)
        return Product.objects.filter(category=category)
    except Category.DoesNotExist:
        return None