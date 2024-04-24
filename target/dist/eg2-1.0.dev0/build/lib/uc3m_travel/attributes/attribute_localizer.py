"""Module for validating the localizer"""
from src.main.python.uc3m_travel.attributes.attribute import Attribute

# pylint: disable=too-few-public-methods
class Localizer(Attribute):
    """Class to validate the localizer attribute"""
    def __init__(self, attr_value):
        super().__init__()
        self._validation_pattern = r'^[a-fA-F0-9]{32}$'
        self._error_message = "Invalid localizer"
        self._attr_value = self._validate(attr_value)
