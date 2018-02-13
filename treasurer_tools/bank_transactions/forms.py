"""Forms for the financial_codes app"""

from django import forms
from django.core.exceptions import ValidationError
from django.forms import inlineformset_factory

from documents.forms import AttachmentMatchForm, NewAttachmentForm
from documents.models import BankStatementMatch
from .models import Statement, BankTransaction


class StatementForm(forms.ModelForm):
    """Form to add and edit transactions"""

    class Meta:
        model = Statement
        fields = [
            "account",
            "date_start",
            "date_end"
        ]

    def clean(self):
        form_data = self.cleaned_data

        # Check that dates are available
        try:
            date_start = form_data["date_start"]
            date_end = form_data["date_end"]
        except KeyError:
            date_start = None
            date_end = None

        # If dates are available, check if start is after end
        if date_start and date_end:
            if date_start > date_end:
                raise ValidationError({
                    "date_end": "The end date must occur after the start date."
                })

        return form_data

class BankTransactionForm(forms.ModelForm):
    """Form for adding and editing bank transactions"""
    class Meta:
        model = BankTransaction
        fields = [
            "date_transaction",
            "description_bank",
            "description_user",
            "amount_debit",
            "amount_credit",
        ]

    def clean(self):
        form_data = self.cleaned_data

        # Check that the amounts are available
        try:
            amount_debit = form_data["amount_debit"]
        except KeyError:
            amount_debit = 0

        try:
            amount_credit = form_data["amount_credit"]
        except KeyError:
            amount_credit = 0

        # If amounts are available, ensure one is 0
        if amount_debit == 0 and amount_credit == 0:
            raise ValidationError({
                "amount_debit": "Please enter a debit or credit value."
            })
        elif amount_debit != 0 and amount_credit != 0:
            raise ValidationError({
                "amount_credit": "A single transaction cannot have both debit and credit amounts entered."
            })

        return form_data

BankTransactionFormSet = inlineformset_factory(
    Statement,
    BankTransaction,
    form=BankTransactionForm,
    extra=1,
    can_delete=True,
)

AttachmentMatchFormSet = inlineformset_factory(
    Statement,
    BankStatementMatch,
    form=AttachmentMatchForm,
    extra=0,
    min_num=0,
    max_num=10,
    can_delete=True,
)

class NewBankAttachmentForm(NewAttachmentForm):
    def __init__(self, *args, **kwargs):
        super(NewAttachmentForm, self).__init__(*args, **kwargs)
        self.fields["files"].help_text="Documentation/files for this bank statement"
        self.fields["files"].label="Bank statement attachments",
        self.fields["files"].prefix = "newattachment"
