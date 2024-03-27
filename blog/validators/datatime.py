from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

class DateTimeValidator:
    def __init__(self, future: bool):
        self.future = future

    def __call__(self, value):
        if self.future:
            self._validate_future(value)
        else:
            self._validate_past(value)

    def _validate_future(self, value):
        if value <= timezone.now():
            raise ValidationError(_("The datetime must be in the future."))

    def _validate_past(self, value):
        if value >= timezone.now():
            raise ValidationError(_("The datetime must be in the past."))

    def serialize(self):
        return {'future': self.future}

    @classmethod
    def deserialize(cls, data):
        return cls(**data)

    def deconstruct(self):
        path = 'store.validators.DateTimeValidator'
        args = (self.future,)
        kwargs = {}
        return path, args, kwargs
