from src.main.python.uc3m_travel.attributes.attribute import Attribute

class Name(Attribute):
    """Class to validate the name attribute"""
    def __init__(self, attr_value):
        self._validation_pattern = r"^(?=^.{10,50}$)([a-zA-Z]+(\s[a-zA-Z]+)+)$"
        self._error_message = "Invalid name format"
        self._attr_value = self._validate(attr_value)
