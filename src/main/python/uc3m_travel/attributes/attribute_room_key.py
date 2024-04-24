"""Module for validating the room key"""
from src.main.python.uc3m_travel.attributes.attribute import Attribute

# pylint: disable=too-few-public-methods
class RoomKey(Attribute):
    """Class to validate the room key attribute"""
    def __init__(self, attr_value):
        super().__init__()
        self._validation_pattern = r'^[a-fA-F0-9]{64}$'
        self._error_message = "Invalid room key format"
        self._attr_value = self._validate(attr_value)
