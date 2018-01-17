import json

from bank_transactions.models import BankTransaction, ReconciliationMatch
from transactions.models import Transaction

class BankReconciliation(object):
    """Object to process bank transaction reconciliation"""
    def create_json_data(self, raw_data):
        # Check for proper JSON data
        try:
            json_data = json.loads(raw_data)
        except ValueError:
            json_data = {"financial_ids": [], "bank_ids": []}
            self.errors["post_data"].append("Invalid data submitted to server.")

        return json_data

    def is_valid(self):
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
            for financial_id in financial_ids:
                # Checks that financial ID exists
                if Transaction.objects.filter(id=financial_id).exists():
                   # Check that this transaction is not already matched
                   if ReconciliationMatch.objects.filter(financial_transaction_id=financial_id).exists():
                       valid = False
                       self.errors["financial_id"].append(
                           (
                               "{} is already reconciled. "
                               "Unmatch the transaction before reassigning it."
                            ).format(str(Transaction.objects.get(id=financial_id)))
                        )
                else:
                    valid = False
                    self.errors["financial_id"].append(
                        (
                            "{} is not a valid financial transaction ID. "
                            "Please make a valid selection."
                        ).format(financial_id)
                    )

        # Check that each bank_id exists
        if bank_ids:
            for bank_id in bank_ids:
                # Check that the bank ID exists
                if BankTransaction.objects.filter(id__in=bank_ids).exists():
                    if ReconciliationMatch.objects.filter(bank_transaction_id=bank_id).exists():
                       valid = False
                       self.errors["bank_id"].append(
                           (
                               "{} is already reconciled. "
                               "Unmatch the transaction before reassigning it."
                            ).format(str(BankTransaction.objects.get(id=bank_id)))
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
        
    def create_matches(self):
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

    def __init__(self, raw_data):
        self.success = {"financial_id": [], "bank_id": [],}
        self.errors = {"post_data": [], "financial_id": [], "bank_id": [],}
        self.json_data = self.create_json_data(raw_data)
