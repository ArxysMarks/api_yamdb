from django.core.exceptions import ValidationError
from django.utils import timezone


def validate_year(year):
    current_year = timezone.now().year
    if year > current_year:
        raise ValidationError(
            'На сайте нельзя публиковать произведения из будущего')
    return year
