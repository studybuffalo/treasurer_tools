"""Test cases for the bank_transaction app"""

import tempfile
from unipath import Path

from django.core.files import File
from django.test import TestCase

from documents.models import Attachment


class AttachmentModelTest(TestCase):
    """Test functions for the Institution model"""

    def test_string_representation_regular(self):
        """Tests string representation works for normal name lengths"""
        temp_file = tempfile.NamedTemporaryFile(suffix=".pdf")
        attachment = Attachment.objects.create(
            location = temp_file.name
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
            location = temp_file.name
        )

        self.assertEqual(
            str(attachment),
            "0-1-2-3-4-5-6-7-8-9-10-11-12-13-14-15-16-17-18-19-20-21-22-23-24-25..."
        )
