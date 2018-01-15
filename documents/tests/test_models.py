"""Test cases for the bank_transaction app"""

from django.test import TestCase

from documents.models import Attachment

class AttachmentModelTest(TestCase):
    """Test functions for the Institution model"""
    # pylint: disable=no-member,protected-access
    
    fixtures = [
        "documents/tests/fixtures/attachment.json",
    ]

    def test_string_representation_regular(self):
        """Tests string representaton works for normal name lengths"""
        attachment = Attachment.objects.get(id=1)

        self.assertEqual(
            str(attachment),
            "test.pdf"
        )
    
    def test_string_representation_long(self):
        """Tests string representaton works for long name lengths"""
        attachment = Attachment.objects.get(id=2)

        self.assertEqual(
            str(attachment),
            "0-1-2-3-4-5-6-7-8-9-10-11-12-13-14-15-16-17-18-19-20-21-22-23-24-25..."
        )
