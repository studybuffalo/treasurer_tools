"""Extending the Django Multiupload widget to fix the render issue."""
from django import forms
from multiupload import fields

class MultiUploadMetaInput(forms.ClearableFileInput):
   """Copying from repo that hasn't be pushed to PyPi.

        See: https://github.com/Chive/django-multiupload/blob/master/multiupload/fields.py
   """
    def __init__(self, *args, **kwargs):
        self.multiple = kwargs.pop('multiple', True)
        super(MultiUploadMetaInput, self).__init__(*args, **kwargs)

    def render(self, name, value, attrs=None, renderer=None):
        if self.multiple:
            attrs['multiple'] = 'multiple'

        return super(MultiUploadMetaInput, self).render(name, value, attrs, renderer)

    def value_from_datadict(self, data, files, name):
        if hasattr(files, 'getlist'):
            return files.getlist(name)

        value = files.get(name)

        if isinstance(value, list):
            return value

        return [value]

class MultiFileField(fields.MultiFileField):
    """Adding the overriden widget to the field."""
    def __init__(self, *args, **kwargs):
        super(MultiFileField, self).__init__(*args, **kwargs)
        self.widget = MultiUploadMetaInput(
            attrs=kwargs.pop('attrs', {}),
            multiple=(self.max_num is None or self.max_num > 1),
        )
