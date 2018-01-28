"""Objects and functions supporting bank_transactions app"""
import json

from bank_transactions.models import BankTransaction
from transactions.models import Transaction

from .models import ReconciliationMatch

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
            if Transaction.objects.filter(id=financial_id).exists():
                # Performs additional testing for match/unmatch
                if self.function_type == "match":
                    if ReconciliationMatch.objects.filter(financial_transaction_id=financial_id).exists():
                        valid = False
                        self.errors["financial_id"].append(
                            (
                                "{} is already reconciled. "
                                "Unmatch the transaction before reassigning it."
                            ).format(str(Transaction.objects.get(id=financial_id)))
                        )
                elif self.function_type == "unmatch":
                    if ReconciliationMatch.objects.filter(financial_transaction_id=financial_id).exists() is False:
                        valid = False
                        self.errors["financial_id"].append(
                            "{} is not a matched transaction.".format(
                                str(Transaction.objects.get(id=financial_id))
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
            # Check that the bank ID exists
            if BankTransaction.objects.filter(id__in=bank_ids).exists():
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
        except KeyError:
            financial_ids = []

            valid = False
            self.errors["financial_id"].append("Please select at least one financial transaction.")
        
        # Check for bank_ids data
        try:
            bank_ids = self.json_data["bank_ids"]
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
                    financial_transaction=Transaction.objects.get(id=financial_id),
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
