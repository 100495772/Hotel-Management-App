"""Module for validating the room type"""
from src.main.python.uc3m_travel.attributes.attribute import Attribute

# pylint: disable=too-few-public-methods
class RoomType(Attribute):
    """Class to validate the room type attribute"""
    def __init__(self, attr_value):
        super().__init__()
        self._validation_pattern = r"(SINGLE|DOUBLE|SUITE)"
        self._error_message = "Invalid roomtype value"
        self._attr_value = self._validate(attr_value)
