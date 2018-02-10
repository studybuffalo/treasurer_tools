"""Objects and functions supporting bank_transactions app"""
import json

from django.core.exceptions import ValidationError
from django.db.models import Q

from bank_transactions.models import BankTransaction
from financial_transactions.models import FinancialTransaction

from bank_reconciliation.models import ReconciliationMatch


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

    # Retrieves all financial transactions between the specified dates
    if transaction_type == "financial":
        try:
            transactions = FinancialTransaction.objects.filter(
                Q(date_submitted__gte=date_start) & Q(date_submitted__lte=date_end)
            )
        except ValidationError:
            json_data["errors"] = {
                "date_start": "Provided date(s) not in valid format ('yyyy-mm-dd').",
                "date_end": "Provided date(s) not in valid format ('yyyy-mm-dd').",
            }

            return json_data

        transaction_list = []

        for transaction in transactions:
            transaction_list.append({
                "transaction": str(transaction),
                "id": transaction.id,
                "total": transaction.total,
                "reconciled": transaction.rm_financial_transaction.all().exists()
            })

        json_data["data"] = transaction_list

    # Retrieve all bank transactions between the specified dates
    elif transaction_type == "bank":
        try:
            transactions = BankTransaction.objects.filter(
                Q(date_transaction__gte=date_start) & Q(date_transaction__lte=date_end)
            )
        except ValidationError:
            json_data["errors"] = {
                "date_start": "Provided date(s) not in valid format ('yyyy-mm-dd').",
                "date_end": "Provided date(s) not in valid format ('yyyy-mm-dd').",
            }
            return json_data

        transaction_list = []

        for transaction in transactions:
            transaction_list.append({
                "transaction": str(transaction),
                "id": transaction.id,
                "debit": transaction.amount_debit,
                "credit": transaction.amount_credit,
                "reconciled": transaction.rm_bank_transaction.all().exists()
            })

        json_data["data"] = transaction_list

    return json_data

class BankReconciliation(object):
    """Object to process bank transaction reconciliation"""
    # pylint: disable=no-member
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
                entry_exists = FinancialTransaction.objects.filter(id=financial_id).exists()
            except ValueError:
                entry_exists = False

            if entry_exists:
                # Performs additional testing for match/unmatch
                if self.function_type == "match":
                    if ReconciliationMatch.objects.filter(financial_transaction_id=financial_id).exists():
                        valid = False
                        self.errors["financial_id"].append(
                            (
                                "{} is already reconciled. "
                                "Unmatch the transaction before reassigning it."
                            ).format(str(FinancialTransaction.objects.get(id=financial_id)))
                        )
                elif self.function_type == "unmatch":
                    if ReconciliationMatch.objects.filter(financial_transaction_id=financial_id).exists() is False:
                        valid = False
                        self.errors["financial_id"].append(
                            "{} is not a matched transaction.".format(
                                str(FinancialTransaction.objects.get(id=financial_id))
                            )
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
                entry_exists = BankTransaction.objects.filter(id__in=bank_ids).exists()
            except ValueError:
                entry_exists = False

            # Check that the bank ID exists
            if entry_exists:
                if self.function_type == "match":
                    if ReconciliationMatch.objects.filter(bank_transaction_id=bank_id).exists():
                        valid = False
                        self.errors["bank_id"].append(
                            (
                                "{} is already reconciled. "
                                "Unmatch the transaction before reassigning it."
                            ).format(str(BankTransaction.objects.get(id=bank_id)))
                        )
                elif self.function_type == "unmatch":
                    if ReconciliationMatch.objects.filter(bank_transaction_id=bank_id).exists() is False:
                        valid = False
                        self.errors["bank_id"].append(
                            "{} is not a matched transaction.".format(
                                str(BankTransaction.objects.get(id=bank_id))
                            )
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
        # pylint: disable=too-many-branches
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
        # Cycle through each financial transaction
        for financial_id in self.json_data["financial_ids"]:
            # Cycle through each bank transaction
            for bank_id in self.json_data["bank_ids"]:
                # Create the match
                ReconciliationMatch.objects.create(
                    financial_transaction=FinancialTransaction.objects.get(id=financial_id),
                    bank_transaction=BankTransaction.objects.get(id=bank_id)
                )

        # Return the ids that were successfully matched
        self.success["financial_id"] = self.json_data["financial_ids"]
        self.success["bank_id"] = self.json_data["bank_ids"]

    def delete_matches(self):
        """Removes matches between provided financial and bank transactions"""

        # Remove any matches with the provided financial ids
        financial_matches = ReconciliationMatch.objects.filter(
            financial_transaction_id__in=self.json_data["financial_ids"]
        )
        financial_matches.delete()

        # Remove any matches with the provided bank ids
        bank_matches = ReconciliationMatch.objects.filter(
            bank_transaction_id__in=self.json_data["bank_ids"]
        )
        bank_matches.delete()

        # Return the ids that were successfully deleted
        self.success["financial_id"] = self.json_data["financial_ids"]
        self.success["bank_id"] = self.json_data["bank_ids"]

    def __init__(self, raw_data, function_type):
        self.function_type = function_type
        self.success = {"financial_id": [], "bank_id": [],}
        self.errors = {"post_data": [], "financial_id": [], "bank_id": [],}
        self.json_data = self.create_json_data(raw_data)
