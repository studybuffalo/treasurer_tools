"""Forms for the financial_codes app"""

from django import forms
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.forms import inlineformset_factory, ValidationError
from django.shortcuts import get_object_or_404
from django.utils import timezone
from custom_multiupload.widgets import MultiFileField

from financial_codes.models import FinancialCodeSystem, BudgetYear, FinancialCode
from documents.models import Attachment, FinancialTransactionMatch

from .models import FinancialTransaction, Item, FinancialCodeMatch
from .widgets import FinancialCodeWithYearID

class CompiledForms(object):
    """Forms and functions for the add/edit transaction/item/code views"""
    class TransactionLevel(object):
        """Holds transaction form and related item formsets"""
        def __init__(self):
            self.transaction_form = None
            self.item_formset = None
            self.item_formsets = []
            self.new_attachment_form = None
            self.old_attachment_formset = None

    class ItemLevel(object):
        """Holds itemformset and related financial code forms"""
        def __init__(self, **kwargs):
            self.item_formset = kwargs.pop("item_formset", None)
            self.financial_code_forms = kwargs.pop("financial_code_forms", None)

    class FinancialCodeLevel(object):
        """Holds financial code forms and other related data"""
        def __init__(self, **kwargs):
            self.system = kwargs.pop("financial_code_system", None)
            self.form = kwargs.pop("financial_code_form", None)

    def __set_financial_code_data(self, item_id, system_id, prefix):
        """Adds financial code data to the POST data to populate form"""
        if self.request_type == "GET":
            # If item ID, this is the initial edit form generation
            if item_id:
                # Retrieve all financial code match entries for this item ID
                try:
                    match_instances = FinancialCodeMatch.objects.filter(item=Item.objects.get(id=item_id))
                except ObjectDoesNotExist:
                    match_instances = []
                    data = None

                # Cycle through each match instance
                for match in match_instances:
                    data = None

                    # Get the budget year for this match instance
                    budget_year = match.financial_code.financial_code_group.budget_year

                    # Update data to the match instance matching provided ID
                    if budget_year.financial_code_system.id == system_id:
                        data = {
                            "{}-financial_code_match_id".format(prefix): match.id,
                            "{}-budget_year".format(prefix): budget_year.id,
                            "{}-code".format(prefix): match.financial_code.id,
                        }

                        break

            # No item ID = initial add form generation
            else:
                data = None
        elif self.request_type == "POST":
            # POST request - use POST data
            data = self.data

        return data

    def create_financial_code_forms(self, item_form_id, item_id, **kwargs):
        """Creates financial code forms required for item formset"""
        # Setup any of the option arguments
        transaction_date = kwargs.pop("transaction_date", timezone.now())

        # Find all the systems encompassing the provided date
        try:
            financial_code_systems = FinancialCodeSystem.objects.filter(
                Q(date_start__lte=transaction_date),
                (Q(date_end=None) | Q(date_end__gte=transaction_date))
            )
        except ValidationError:
            financial_code_systems = []

        # Create a FinancialCodeAssignmentForm for each system
        financial_code_forms = []

        for form_id, system in enumerate(financial_code_systems):
            # Setup the proper prefix for the form fields
            prefix = "items-{}-coding_set-{}".format(item_form_id, form_id)

            data = self.__set_financial_code_data(item_id, system.id, prefix)

            financial_code_form = FinancialCodeAssignmentForm(
                data,
                prefix=prefix,
                transaction_type=self.transaction_type,
                system=system,
            )

            # Add the form and a system title to the list
            financial_code_forms.append(self.FinancialCodeLevel(
                financial_code_system=system.title,
                financial_code_form=financial_code_form
            ))

        return financial_code_forms

    def __create_post_forms(self, kwargs):
        """Creates add/edit transaction forms for a POST request"""
        # Setup object to hold all the data
        compiled_forms = self.TransactionLevel()

        # Get any transaction ID (if provided)
        transaction_id = kwargs.pop("transaction_id", None)

        # If transaction ID present, retrieve database values
        if transaction_id:
            # Get the transaction object for this ID
            transaction_instance = get_object_or_404(FinancialTransaction, id=transaction_id)

            # Create the transaction form with the Transaction instance
            compiled_forms.transaction_form = TransactionForm(
                self.data,
                instance=transaction_instance,
            )

            # Create the item formset with the Transaction instance
            compiled_forms.item_formset = ItemFormSet(
                self.data,
                instance=transaction_instance
            )

            # Add attachment form
            compiled_forms.new_attachment_form = NewAttachmentForm(
                self.data,
                self.files,
            )

            # Add attachment formset
            compiled_forms.old_attachment_formset = AttachmentFormSet(
                self.data,
                instance=transaction_instance
            )

        # No database values - create blank form
        else:
            # Create the transaction form and specify transaction type
            compiled_forms.transaction_form = TransactionForm(
                self.data,
                initial={"transaction_type": self.transaction_type},
            )

            # Create the item formset
            compiled_forms.item_formset = ItemFormSet(self.data)

            # Add attachment form
            compiled_forms.new_attachment_form = NewAttachmentForm(
                self.data,
                self.files,
            )

            # Add attachment formset
            compiled_forms.old_attachment_formset = AttachmentFormSet(self.data)

        # Break item formsets into individual forms & group with code forms
        for item_form_id, item_formset in enumerate(compiled_forms.item_formset):
            # Get any item instance ID
            item_instance_id = item_formset["id"].value()

            compiled_forms.item_formsets.append(self.ItemLevel(
                item_formset=item_formset,
                financial_code_forms=self.create_financial_code_forms(
                    item_form_id,
                    item_instance_id,
                    transaction_date=item_formset["date_item"].value(),
                )
            ))

        return compiled_forms

    def __create_get_forms(self, kwargs):
        """Creates add/edit transaction forms for a GET request"""
        # Setup object to hold all the data
        compiled_forms = self.TransactionLevel()

        # Get any transaction ID (if provided)
        transaction_id = kwargs.pop("transaction_id", None)

        # If transaction ID present, retrieve database values
        if transaction_id:
            # Get the transaction object for this ID
            transaction_instance = get_object_or_404(FinancialTransaction, id=transaction_id)

            # Create the transaction form with the Transaction instance
            compiled_forms.transaction_form = TransactionForm(
                instance=transaction_instance,
            )

            # Create item formset with Transaction instance
            compiled_forms.item_formset = ItemFormSet(instance=transaction_instance)

            # Add attachment form
            compiled_forms.new_attachment_form = NewAttachmentForm()

            # Add attachment formset
            compiled_forms.old_attachment_formset = AttachmentFormSet(
                instance=transaction_instance
            )

        # No database values - create blank form
        else:
            # Create the transaction form and specify transaction type
            compiled_forms.transaction_form = TransactionForm(
                initial={"transaction_type": self.transaction_type},
            )

            # Create the item formset
            compiled_forms.item_formset = ItemFormSet()

            # Disable formset delete field
            compiled_forms.item_formset.can_delete = False

            # Add attachment form
            compiled_forms.new_attachment_form = NewAttachmentForm()

            # Add attachment formset
            compiled_forms.old_attachment_formset = AttachmentFormSet()

        # Break item formsets into individual forms & group with code forms
        for item_form_id, item_formset in enumerate(compiled_forms.item_formset):
            # Get any item instance ID
            item_instance_id = item_formset["id"].value()

            compiled_forms.item_formsets.append(self.ItemLevel(
                item_formset=item_formset,
                financial_code_forms=self.create_financial_code_forms(
                    item_form_id,
                    item_instance_id,
                    transaction_date=item_formset["date_item"].value(),
                )
            ))

        return compiled_forms

    def assemble_forms(self, kwargs):
        """Assembles all levels of the required forms"""
        if self.request_type == "POST":
            compiled_forms = self.__create_post_forms(kwargs)
        else:
            # Assumed to be a GET request (as per view)
            compiled_forms = self.__create_get_forms(kwargs)

        return compiled_forms

    def assemble_empty_financial_code_form(self):
        """Assembles empty set of financial code forms (like .empty_form())"""
        # Set the item date as today
        date_item = timezone.now()

        # Find all the systems encompassing the provided date
        financial_code_systems = FinancialCodeSystem.objects.filter(
            Q(date_start__lte=date_item),
            (Q(date_end=None) | Q(date_end__gte=date_item))
        )

        # Create a FinancialCodeAssignmentForm for each system
        financial_code_forms = []
        form_id = 0

        for system in financial_code_systems:
            # Setup the proper prefix for the form fields
            prefix = "items-__prefix__-coding_set-{}".format(form_id)

            # Create a financial code form to act as the blank template
            financial_code_form = FinancialCodeAssignmentForm(
                {},
                prefix=prefix,
                transaction_type=self.transaction_type,
                system=system,
            )

            # Remove the errors generated from the code field
            financial_code_form.errors["code"] = financial_code_form.error_class()

            financial_code_forms.append({
                "name": system.title,
                "form": financial_code_form,
            })

            form_id = form_id + 1

        return financial_code_forms

    def is_valid(self):
        """Checks if all forms are valid"""
        valid = True

        # Check if transaction form is valid
        if self.forms.transaction_form.is_valid() is False:
            valid = False

        # Keep count of number of item formset to be submitted
        item_formset_num = len(self.forms.item_formsets)

        # Checks if item formsets and financial code matches are valid
        for item_formset_group in self.forms.item_formsets:
            # Check that item formset is valid
            if item_formset_group.item_formset.is_valid():
                # If valid, check if marked for deletion
                if item_formset_group.item_formset.cleaned_data["DELETE"]:
                    item_formset_num = item_formset_num - 1
            else:
                valid = False

            # Check if financial code forms are valid
            for financial_code_form in item_formset_group.financial_code_forms:
                if financial_code_form.form.is_valid() is False:
                    valid = False

        # Check that there is at least one item formset to be submitted
        if item_formset_num <= 0:
            valid = False

        # Check if attachment form is valid
        if self.forms.new_attachment_form.is_valid() is False:
            valid = False

        # Check if the old attachment form is valid
        if self.forms.old_attachment_formset.is_valid() is False:
            valid = False

        return valid

    def save(self):
        """Saves all item formsets and financial code matches"""
        # Save the transaction form
        transaction_instance = self.forms.transaction_form.save()

        # Update the transaction_instance with the proper type
        transaction_instance.transaction_type = self.transaction_type
        transaction_instance.save()

        # Cycle through each item formset
        for item_formset_group in self.forms.item_formsets:
            # Delete any item formset marked for deletion
            if item_formset_group.item_formset.cleaned_data["DELETE"]:
                item_formset_group.item_formset.cleaned_data["id"].delete()
            else:
                # Create the item instance
                saved_item = item_formset_group.item_formset.save(commit=False)

                # Set transaction ID for item item instance
                saved_item.transaction = transaction_instance

                # Save the item formset
                saved_item.save()

                # Get new item ID
                item_id = saved_item.id

                # Cycle through each financial code form
                for financial_code_form in item_formset_group.financial_code_forms:
                    # Get any ID for an exisiting match ID
                    match_id = financial_code_form.form.cleaned_data["financial_code_match_id"]

                    # If a match ID is present, get the original object
                    if match_id:
                        match = get_object_or_404(FinancialCodeMatch, id=match_id)
                    # No match ID - create new instance
                    else:
                        match = FinancialCodeMatch()

                    # Update match instance data and save
                    match.item = Item.objects.get(id=item_id)
                    match.financial_code = FinancialCode.objects.get(
                        id=financial_code_form.form.cleaned_data["code"]
                    )
                    match.save()

        # Save attachment form
        for file in self.forms.new_attachment_form.cleaned_data["attachment_files"]:
            # Save the file to an attachment instance
            attachment_instance = Attachment.objects.create(
                location=file
            )

            # Create record in attachment matching model
            attachment_match = FinancialTransactionMatch(
                transaction=transaction_instance,
                attachment=attachment_instance,
            )
            attachment_match.save()

        # Delete any old attachments
        for attachment_form in self.forms.old_attachment_formset:
            try:
                if attachment_form.cleaned_data["DELETE"]:
                    attachment_form.cleaned_data["id"].delete()
            except KeyError:
                pass

    def compile_css(self):
        """Generates CSS to accomodate variable form fields"""
        # Initial column widths
        width_add = ["9rem", "4fr", "8rem", "8rem"]
        width_edit = ["9rem", "4fr", "8rem", "8rem"]

        # Initial area names
        area_add = ["date", "description", "amount", "gst"]
        area_edit = ["date", "description", "amount", "gst"]

        # Cycle through each financial code system to generate the css
        system_details = []

        for system in FinancialCodeSystem.objects.all():
            # Add the widths
            width_add.extend(("2fr", "2fr"))
            width_edit.extend(("2fr", "2fr"))

            # Add the area names
            name_system = system.title.replace(" ", "_").lower()

            name_year = "{}-year".format(name_system)
            name_code = "{}-code".format(name_system)

            area_add.extend((name_year, name_code))
            area_edit.extend((name_year, name_code))

            # Add the system details
            system_details.append({
                "label": system.title,
                "css": name_system,
                "year": name_year,
                "code": name_code,
            })

        # Add the delete details for edit
        width_edit.append("5rem")
        area_edit.append("delete")

        return {
            "width_add": " ".join(width_add),
            "width_edit": " ".join(width_edit),
            "area_add": " ".join(area_add),
            "area_edit": " ".join(area_edit),
            "system_details": system_details,
        }

    def __init__(self, transaction_type="EXPENSE", request_type="GET", data=None, files=None, **kwargs):
        self.transaction_type = "e" if transaction_type.upper() == "EXPENSE" else "r"
        self.request_type = request_type.upper()
        self.data = data
        self.files = files
        self.forms = self.assemble_forms(kwargs)
        self.empty_financial_code_form = self.assemble_empty_financial_code_form()
        self.css = self.compile_css()

class TransactionForm(forms.ModelForm):
    """Form to add and edit transactions"""
    class Meta:
        model = FinancialTransaction

        fields = [
            "payee_payer",
            "memo",
            "submitter",
            "date_submitted",
        ]

class ItemForm(forms.ModelForm):
    """Form to add and edit Items"""
    class Meta:
        model = Item
        fields = [
            "date_item",
            "description",
            "amount",
            "gst",
        ]

ItemFormSet = inlineformset_factory(
    FinancialTransaction,
    Item,
    form=ItemForm,
    extra=0,
    min_num=1,
    validate_min=True,
    can_delete=True,
)

class FinancialCodeAssignmentForm(forms.Form):
    """Form to assign a financial code"""
    financial_code_match_id = forms.IntegerField(
        required=False,
        widget=forms.HiddenInput,
    )
    budget_year = forms.ChoiceField(
        choices=[],
        label="Budget year",
        required=False,
    )
    code = forms.ChoiceField(
        choices=[],
        label="Financial code",
        widget=FinancialCodeWithYearID,
    )

    def __init__(self, *args, **kwargs):
        # Get the financial code system
        financial_code_system = kwargs.pop("system")
        transaction_type = kwargs.pop("transaction_type")

        # Retrieve all the children BudgetYears entries
        budget_years = BudgetYear.objects.filter(
            financial_code_system=financial_code_system
        ).order_by('-date_start')

        # Create a choice list with the budget_years
        budget_year_choices = []

        for year in budget_years:
            budget_year_choices.append((year.id, str(year)))

        # Create a choice list with the budget_years
        groups_and_codes = []

        # Retrieve all the children FinancialCodeGroup entries
        for year in budget_years:
            groups = year.financialcodegroup_set.filter(type=transaction_type)

            for group in groups:
                code_list = []

                codes = group.financialcode_set.all().order_by("code")

                for code in codes:
                    code_list.append((code.id, str(code)))

                groups_and_codes.append([group.title, code_list])

        # Sort the groups by the first code in each group
        sorted_groups_and_codes = sorted(groups_and_codes, key=lambda x: x[1][0][1])

        # Create the final financial code choice list
        financial_code_choices = [["", "---------"]] + sorted_groups_and_codes

        super(FinancialCodeAssignmentForm, self).__init__(*args, **kwargs)

        # Specify the choices
        self.fields["budget_year"].choices = budget_year_choices
        self.fields["code"].choices = financial_code_choices

class NewAttachmentForm(forms.Form):
    """Form to handle file attachments to transaction"""
    attachment_files = MultiFileField(
        help_text="Documentation/files for this transaction",
        label="Transaction attachments",
        max_file_size=1024*1024*10,
        max_num=20,
        required=False,
    )

    prefix = "newattachment"

class OldAttachmentForm(forms.ModelForm):
    """Form to view and delete attachments"""
    class Meta:
        model = FinancialTransactionMatch
        fields = [
            "attachment",
        ]
        widgets = {
            "attachment": forms.HiddenInput(),
        }

AttachmentFormSet = inlineformset_factory(
    FinancialTransaction,
    FinancialTransactionMatch,
    form=OldAttachmentForm,
    extra=0,
    min_num=0,
    max_num=20,
    can_delete=True,
)
