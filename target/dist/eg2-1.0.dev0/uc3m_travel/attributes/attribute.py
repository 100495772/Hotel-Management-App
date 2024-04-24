"""Module for validating attributes"""
import re
from src.main.python.uc3m_travel.hotel_management_exception import HotelManagementException
class Attribute():
    """Abstract class to validate the input parameters for F1, F2 and F3 methods"""

    def __init__(self):
        self._validation_pattern = r""
        self._error_message = " "
        self._attr_value = " "

    def _validate (self, attr_value):
        """ Attribute validation definition """
        myregex = re.compile(self._validation_pattern)
        regex_matches = myregex.fullmatch(attr_value)
        if not regex_matches:
            raise HotelManagementException(self._error_message)
        return attr_value

    @property
    def value(self):
        """ returns attr_value """
        return self._attr_value

    @value.setter
    def value(self, attr_value):
        self._attr_value = self._validate(attr_value)

    def __str__(self):
        """ Returns a string representation of the attribute value """
        return str(self._attr_value)
