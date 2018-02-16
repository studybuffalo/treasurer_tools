"""Test cases for the documents app"""

import tempfile
from unipath import Path

from django.test import TestCase

from documents.models import Attachment, BankStatementMatch
from .utils import create_bank_statement

class AttachmentModelTest(TestCase):
    """Test functions for the Attachment model"""

    def test_string_representation_regular(self):
        """Tests string representation works for normal name lengths"""
        temp_file = tempfile.NamedTemporaryFile(suffix=".pdf")
        attachment = Attachment.objects.create(
            location=temp_file.name
        )

        self.assertEqual(
            str(attachment),
            Path(temp_file.name).name
        )

    def test_string_representation_long(self):
        """Tests string representaton works for long name lengths"""
        temp_file = tempfile.NamedTemporaryFile(
            prefix="0-1-2-3-4-5-6-7-8-9-10-11-12-13-14-15-16-17-18-19-20-21-22-23-24-25-26-27-28-29-30",
            suffix=".pdf"
        )
        attachment = Attachment.objects.create(
            location=temp_file.name
        )

        self.assertEqual(
            str(attachment),
            "0-1-2-3-4-5-6-7-8-9-10-11-12-13-14-15-16-17-18-19-20-21-22-23-24-25..."
        )

class BankStatementMatchTest(TestCase):
    """Tests for the BankStatementMatch model"""
    def test_string_representation(self):
        """Tests string representation of attachment match"""
        # Create a new match instance
        temp_file = tempfile.NamedTemporaryFile(suffix=".pdf")
        attachment = Attachment.objects.create(
            location=temp_file.name
        )

        statement = create_bank_statement()

        match = BankStatementMatch.objects.create(
            statement=statement,
            attachment=attachment,
        )

        self.assertEqual(
            str(match),
            "{} - {}".format(statement, attachment)
        )
