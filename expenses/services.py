from .models import Category, User

DEFAULT_CATEGORIES = (
    "Забота о себе", "Зарплата", "Здоровье и фитнес", "Кафе и рестораны",
    "Машина", "Образование", "Отдых и развлечения", "Платежи, комиссии",
    "Покупки: одежда, техника", "Продукты", "Проезд"
)


def create_default_category_for_user(user: User) -> None:
    """Создает категории по умолчанию"""
    categories = [Category(name=category, user=user) for category in DEFAULT_CATEGORIES]
    Category.objects.bulk_create(categories)
