from django.forms import model_to_dict


class ModelChangeDetectMixin(object):
    """
    Mixin that detects changes in model fields.
    """

    def __init__(self, *args, **kwargs):
        super(ModelChangeDetectMixin, self).__init__(*args, **kwargs)
        self.__initial = self._dict

    @property
    def diff(self):
        d1 = self.__initial
        d2 = self._dict
        diffs = [(k, (v, d2[k])) for k, v in d1.items() if v != d2[k]]
        return dict(diffs)

    @property
    def has_changed(self):
        return bool(self.diff)

    @property
    def changed_fields(self):
        return self.diff.keys()

    def get_field_diff(self, field_name):
        """
        Returns a diff for field if it's changed and None otherwise.
        """
        return self.diff.get(field_name, None)

    def save(self, *args, **kwargs):
        """
        Saves model and set initial state.
        """
        super(ModelChangeDetectMixin, self).save(*args, **kwargs)
        self.__initial = self._dict

    @property
    def _dict(self):
        return model_to_dict(self, fields=[field.name for field in
                                           self._meta.fields])


class ErrorHandlerMixin(object):
    def __init__(self) -> None:
        self.errors = list()

    def update_errors(self, error_message):
        self._errors.append({'error': error_message})

    @property
    def errors(self) -> dict:
        if len(self._errors):
            return self._errors
