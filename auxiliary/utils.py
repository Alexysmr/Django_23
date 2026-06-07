from django.core.mail import send_mail
from django.conf import settings


def send_100_views_congratulation(obj):
    """Отправка сообщения на эл.почту в случае достижения числа просмотров поста 100"""
    try:
        send_mail(
            subject=f'🎉 "Article "{obj.title}" reached 100 views!',
            message=f'Your article has {obj.number_of_views} views.\n-- SkyPro blog bot',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.EMAIL_HOST_USER],
            fail_silently=False,
        )
    except Exception as e:
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f'Ошибка отправки письма: {e}')


def user_in_groups(user, group_list):
    """ Проверяет, входит ли пользователь хотя бы в одну из указанных групп.
    Args:
        user: объект User (или AnonymousUser)
        group_list: список имён групп (например, ['Контент-менеджер', 'Редактор'])
    Returns:
        bool: True, если пользователь аутентифицирован и состоит хотя бы в одной из групп.
    """
    if not user.is_authenticated:
        return False
    return user.groups.filter(name__in=group_list).exists()