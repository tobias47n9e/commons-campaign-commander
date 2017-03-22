"""
Contains the Campaign Commander validators.
"""

from django.core.exceptions import ValidationError


def validate_wikidata_id(value):
    """
    Validates if a value is a valid Wikidata-ID.
    """
    if len(value) < 2 or value[0] != 'Q' or not value[1:].isdigit():
        raise ValidationError('Not a valid Wikidata ID',
                              params={'value': value})
