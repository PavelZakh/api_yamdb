from django.utils import timezone
from django.core.exceptions import ValidationError


def year_validator(value):
    if value < 1900 or value > timezone.now().year:
        raise ValidationError(
            f'{value} is not a correct year!'
        )
