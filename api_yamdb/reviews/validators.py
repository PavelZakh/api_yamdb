import datetime

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def my_year_validator(value):
    if value < 1900 or value > datetime.datetime.now().year:
        raise ValidationError(
            _('%(value)s is not a correcrt year!'),
            params={'value': value},
        )
