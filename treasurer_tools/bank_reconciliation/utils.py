"""Objects and functions supporting bank_transactions app"""
import json

from bank_reconciliation.models import ReconciliationGroup
from bank_transactions.models import BankTransaction
from django.core.exceptions import ValidationError
from django.db.models import Q
from financial_transactions.models import FinancialTransaction


def return_transactions_as_json(request):
    """Returns bank and financial transactions as JSON data"""
    # The blank json_data variable to return
    json_data = {
        "type": None,
        "data": None,
        "errors": None
    }

    # Collect the variables from the GET request
    transaction_type = request.GET.get("transaction_type", None)
    date_start = request.GET.get("date_start", None)
    date_end = request.GET.get("date_end", None)

    # Checks that a valid transaction type was provided
    if not (transaction_type == "financial" or transaction_type == "bank"):
        json_data["errors"] = {"transaction_type": "Invalid transaction type provided."}

        return json_data
    else:
        json_data["type"] = transaction_type

    # Checks that start date was provided
    if not date_start:
        json_data["errors"] = {"date_start": "Must specify start date."}

        return json_data

    # Checks that end date was provided
    if not date_end:
        json_data["errors"] = {"date_end": "Must specify end date."}

        return json_data

    # Retrieves all unreconciled financial transactions between the specified dates
    if transaction_type == "financial":
        try:
            transactions = FinancialTransaction.objects.filter(
                Q(date_submitted__gte=date_start)
                & Q(date_submitted__lte=date_end)
                & Q(reconciled=None)
            ).order_by("-date_submitted")
        except ValidationError:
            json_data["errors"] = {
                "date_start": "Provided date(s) not in valid format ('yyyy-mm-dd').",
                "date_end": "Provided date(s) not in valid format ('yyyy-mm-dd').",
            }

            return json_data

        transaction_list = []

        for transaction in transactions:
            transaction_list.append({
                "id": transaction.id,
                "date": transaction.date_submitted,
                "type": transaction.get_transaction_type_display().title(),
                "description": "{} - {}".format(transaction.payee_payer, transaction.memo),
                "total": transaction.total,
            })

        json_data["data"] = transaction_list

    # Retrieve all unreconciled bank transactions between the specified dates
    elif transaction_type == "bank":
        try:
            transactions = BankTransaction.objects.filter(
                Q(date_transaction__gte=date_start)
                & Q(date_transaction__lte=date_end)
                & Q(reconciled=None)
            ).order_by("-date_transaction")
        except ValidationError:
            json_data["errors"] = {
                "date_start": "Provided date(s) not in valid format ('yyyy-mm-dd').",
                "date_end": "Provided date(s) not in valid format ('yyyy-mm-dd').",
            }
            return json_data

        transaction_list = []

        for transaction in transactions:
            transaction_list.append({
                "id": transaction.id,
                "date": transaction.date_transaction,
                "description": (
                    transaction.description_user if transaction.description_user else transaction.description_bank
                ),
                "debit": transaction.amount_debit,
                "credit": transaction.amount_credit,
            })

        json_data["data"] = transaction_list

    return json_data

def return_matches_as_json(request):
    """Returns bank and financial transactions as JSON data"""
    # The blank json_data variable to return
    json_data = {
        "data": [],
        "errors": [],
    }

    # Collect the variables from the GET request
    financial_date_start = request.GET.get("financial_date_start", None)
    financial_date_end = request.GET.get("financial_date_end", None)
    bank_date_start = request.GET.get("bank_date_start", None)
    bank_date_end = request.GET.get("bank_date_end", None)

    # Checks that valid dates were provided
    if not financial_date_start:
        json_data["errors"].append({"financial_date_start": "Must specify financial start date."})

    if not financial_date_end:
        json_data["errors"].append({"financial_date_end": "Must specify financial end date."})

    if not bank_date_start:
        json_data["errors"].append({"bank_date_start": "Must specify bank start date."})

    if not bank_date_end:
        json_data["errors"].append({"bank_date_end": "Must specify bank end date."})

    if json_data["errors"]:
        return json_data

    # Retrieve all the matches transactions that meet either date range
    try:
        # Get all the financial transactions in the specified date range
        financial_transactions = list(FinancialTransaction.objects.filter(
            Q(date_submitted__gte=financial_date_start)
            & Q(date_submitted__lte=financial_date_end)
        ).values_list("reconciled", flat=True))

        # Get all the bank transactions in the specified date range
        bank_transactions = list(BankTransaction.objects.filter(
            Q(date_transaction__gte=bank_date_start)
            & Q(date_transaction__lte=bank_date_end)
        ).values_list("reconciled", flat=True))

        # Get a unique list of the IDs
        group_id_list = set(financial_transactions + bank_transactions)

        # Get all the Match Groups containing above transactions
        groups = ReconciliationGroup.objects.filter(id__in=group_id_list)

    except ValidationError:
        json_data["errors"].append({"dates": "Provided date(s) not in valid format ('yyyy-mm-dd')."})

        return json_data

    # Cycle through each group and assemble data to return
    group_data = []

    for group in groups:
        financial_transactions = []
        bank_transactions = []

        for financial_transaction in group.financialtransactions.all():
            financial_transactions.append({
                "date": financial_transaction.date_submitted,
                "type": financial_transaction.get_transaction_type_display().title(),
                "description": "{} - {}".format(
                    financial_transaction.payee_payer, financial_transaction.memo
                ),
                "total": financial_transaction.total,
            })

        for bank_transaction in group.banktransactions.all():
            bank_transactions.append({
                "date": bank_transaction.date_transaction,
                "description": (
                    bank_transaction.description_user
                    if bank_transaction.description_user
                    else bank_transaction.description_bank
                ),
                "debit": bank_transaction.amount_debit,
                "credit": bank_transaction.amount_credit,
            })

        group_data.append({
            "id": group.id,
            "financial_transactions": financial_transactions,
            "bank_transactions": bank_transactions,
        })

    json_data["data"] = group_data
    return json_data

class BankReconciliation(object):
    """Object to process bank transaction reconciliation"""

    def create_json_data(self, raw_data):
        """Converts raw json data to dictionary"""
        # Check for proper JSON data
        try:
            json_data = json.loads(raw_data)
        except ValueError:
            json_data = {"financial_ids": [], "bank_ids": []}
            self.errors["post_data"].append("Invalid data submitted to server.")

        return json_data

    def __is_valid_financial_ids(self, financial_ids):
        """Checks that provided financial_ids are valid"""
        valid = True

        for financial_id in financial_ids:
            # Checks that financial ID exists
            try:
                financial_transaction = FinancialTransaction.objects.get(id=financial_id)
            except FinancialTransaction.DoesNotExist:
                financial_transaction = False
            except ValueError:
                financial_transaction = False

            if financial_transaction:
                # Checks if this entry has already been reconciled
                if financial_transaction.reconciled:
                    valid = False
                    self.errors["financial_id"].append(
                        (
                            "{} is already reconciled. "
                            "Unmatch the transaction before reassigning it."
                        ).format(str(financial_transaction))
                    )
            else:
                valid = False
                self.errors["financial_id"].append(
                    (
                        "{} is not a valid financial transaction ID. "
                        "Please make a valid selection."
                    ).format(financial_id)
                )


        return valid

    def __is_valid_bank_ids(self, bank_ids):
        """Checks that provided bank_ids are valid"""
        valid = True

        for bank_id in bank_ids:
            # Checks that financial ID exists
            try:
                bank_transaction = BankTransaction.objects.get(id=bank_id)
            except BankTransaction.DoesNotExist:
                bank_transaction = False
            except ValueError:
                bank_transaction = False

            # Check that the bank ID exists
            if bank_transaction:
                if bank_transaction.reconciled:
                    valid = False
                    self.errors["bank_id"].append(
                        (
                            "{} is already reconciled. "
                            "Unmatch the transaction before reassigning it."
                        ).format(str(bank_transaction))
                    )
            else:
                valid = False
                self.errors["bank_id"].append(
                    (
                        "{} is not a valid bank transaction ID. "
                        "Please make a valid selection."
                    ).format(bank_id)
                )

        return valid

    def is_valid(self):
        """Checks that provided transaction & banking data is valid"""

        valid = True

        # Check for financial_ids data
        try:
            financial_ids = self.json_data["financial_ids"]

            if len(financial_ids) is 0:
                valid = False
                self.errors["financial_id"].append("Please select at least one financial transaction.")

        except KeyError:
            financial_ids = []

            valid = False
            self.errors["financial_id"].append("Please select at least one financial transaction.")

        # Check for bank_ids data
        try:
            bank_ids = self.json_data["bank_ids"]

            if len(bank_ids) is 0:
                valid = False
                self.errors["bank_id"].append("Please select at least one bank transaction.")

        except KeyError:
            bank_ids = []

            valid = False
            self.errors["bank_id"].append("Please select at least one bank transaction.")

        # Additional validation of financial ID data
        if financial_ids:
            financial_ids_valid = self.__is_valid_financial_ids(financial_ids)

            if financial_ids_valid is False:
                valid = False

        # Check that each bank_id exists
        if bank_ids:
            bank_ids_valid = self.__is_valid_bank_ids(bank_ids)

            if bank_ids_valid is False:
                valid = False

        return valid

    def create_matches(self):
        """Matches provided financial and bank transactions"""
        # Create a reconcilation group
        group = ReconciliationGroup.objects.create()

        # Add the new group to each financial transaction
        for financial_id in self.json_data["financial_ids"]:
            financial_transaction = FinancialTransaction.objects.get(id=financial_id)
            financial_transaction.reconciled = group
            financial_transaction.save()

        # Add the new group to each bank transaction
        for bank_id in self.json_data["bank_ids"]:
            bank_transaction = BankTransaction.objects.get(id=bank_id)
            bank_transaction.reconciled = group
            bank_transaction.save()

        # Return the ids that were successfully matched
        self.success["financial_id"] = self.json_data["financial_ids"]
        self.success["bank_id"] = self.json_data["bank_ids"]

    def __init__(self, raw_data):
        self.success = {"financial_id": [], "bank_id": [],}
        self.errors = {"post_data": [], "financial_id": [], "bank_id": [],}
        self.json_data = self.create_json_data(raw_data)
