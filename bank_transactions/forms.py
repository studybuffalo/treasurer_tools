"""Forms for the financial_codes app"""

from django import forms
from django.forms import Textarea, inlineformset_factory
from multiupload.fields import MultiFileField

from .models import Statement, Institution, BankTransaction, AttachmentMatch


class StatementForm(forms.ModelForm):
    """Form to add and edit transactions"""
    # pylint: disable=missing-docstring,too-few-public-methods

    class Meta:
        model = Statement

        fields = ("account", "date_start", "date_end")

class InstitutionForm(forms.ModelForm):
    """Form to add and edit transactions"""
    # pylint: disable=missing-docstring,too-few-public-methods

    class Meta:
        model = Institution

        fields = ("name", "address", "phone", "fax")
        widgets = {
            "address": Textarea(),
        }
        
BankTransactionFormset = inlineformset_factory(
    Statement,
    BankTransaction,
    fields=(
        "date_transaction",
        "description_bank",
        "description_user",
        "amount_debit",
        "amount_credit",
    ),
    labels={
        "date_transaction": "Transaction date",
        "description_bank": "Bank description",
        "description_user": "Custom description",
        "amount_debit": "Debit amount",
        "amount_credit": "Credit amount",
    },
    extra=1,
    can_delete=True,
)

class AttachmentMatchForm(forms.ModelForm):
    """Model form for attachment matches"""
    # pylint: disable=missing-docstring,too-few-public-methods
    class Meta:
        model = AttachmentMatch
        fields = [
            "attachment",
        ]
        widgets = {
            "attachment": forms.HiddenInput(),
        }
        
AttachmentMatchFormset = inlineformset_factory(
    Statement,
    AttachmentMatch,
    form=AttachmentMatchForm,
    extra=0,
    min_num=0,
    max_num=10,
    can_delete=True,
)

class NewAttachmentForm(forms.Form):
    """Form to handle file attachments to bank statement"""
    files = MultiFileField(
        help_text="Documentation/files for this bank statement",
        label="Bank statement attachments",
        max_file_size=1024*1024*10,
        max_num=10,
        required=False,
    )

    prefix = "newattachment"
