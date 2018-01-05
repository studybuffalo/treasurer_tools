"""Serializers for the financial_codes app"""
from django.core.serializers.json import Serializer

class FinancialCodeSystemSerializer(Serializer):
    def get_dump_object(self, obj):
        return self._current

