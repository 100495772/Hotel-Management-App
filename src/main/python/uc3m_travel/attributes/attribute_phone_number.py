"""Module for validating the phone number"""
from src.main.python.uc3m_travel.attributes.attribute import Attribute

# pylint: disable=too-few-public-methods
class PhoneNumber(Attribute):
    """Class to validate the phone number attribute"""
    def __init__(self, attr_value):
        super().__init__()
        self._validation_pattern = r"^(\+)[0-9]{9}"
        self._error_message = "Invalid phone number format"
        self._attr_value = self._validate(attr_value)
