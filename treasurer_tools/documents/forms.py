"""Forms for the documents app"""

from multiupload.fields import MultiFileField

from django import forms

class NewAttachmentForm(forms.Form):
    """Form to handle file attachments"""
    files = MultiFileField(
        max_file_size=1024*1024*10,
        max_num=10,
        required=False,
    )

    class Meta:
        abstract = True
