from .models import Category

def categories(request):
    """Добавляет список всех категорий в контекст шаблонов"""
    return {
        'all_categories': Category.objects.all()
    }