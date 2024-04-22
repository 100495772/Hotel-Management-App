from src.main.python.uc3m_travel.attributes.attribute import Attribute

class ArrivalDate(Attribute):
    """Class to validate the arrival date"""
    def __init__(self, attr_value):
        self._validation_pattern = r"^(([0-2]\d|-3[0-1])\/(0\d|1[0-2])\/\d\d\d\d)$"
        self._error_message = "Invalid date format"
        self._attr_value = self._validate(attr_value)
