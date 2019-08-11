"""Extending the Django Multiupload widget to fix the render issue."""
from multiupload.fields import MultiFileField as OriginalField

class MultiFileField(OriginalField):
    def render(self, name, value, attrs=None, renderer=None):
        if self.multiple:
            attrs['multiple'] = 'multiple'

        return super(MultiFileField, self).render(name, value, attrs, renderer)
