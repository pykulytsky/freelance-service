from django.core.exceptions import ValidationError
from decimal import Decimal


def validate_age(age):
    if isinstance(age, int):
        if age < 1:
            raise ValidationError(f"Your age is to low({age}), must be at least 1.")
        if age > 120:
            raise ValidationError(f"Your age is to high({age}), must be max 120.")
    else:
        raise ValidationError("Age field must be integer like object")


def percent_validation(percent):
    if isinstance(percent, Decimal):
        if 100 < percent < 0:
            raise ValidationError(f"Percent must be between 0.0 and 100.0 not{percent}") 
    else:
        raise ValidationError("Percent must be decimal like object")


def rating_validator(rating):
    if isinstance(rating, int):
        if rating > 10:
            raise ValidationError("Rating is too height")
    else:
        raise ValidationError("Not supported type of rating")