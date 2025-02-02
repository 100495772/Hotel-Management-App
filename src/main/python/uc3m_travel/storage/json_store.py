"""Module for general methods related to json stores"""
import json
from src.main.python.uc3m_travel.hotel_management_exception import HotelManagementException


class JsonStore():
    """father class containing general methods to store and load json data"""
    def __init__(self):
        pass


    def load_json_list(self, file_store):
        """General method to load the contents of a json file into a data list"""
        # leo los datos del fichero si existe , y si no existe creo una lista vacia
        try:
            with open(file_store, "r", encoding="utf-8", newline="") as file:
                room_key_list = json.load(file)
        # pylint: disable=unused-variable
        except FileNotFoundError as ex:
            room_key_list = []
        except json.JSONDecodeError as ex:
            raise HotelManagementException("JSON Decode Error - Wrong JSON Format") from ex
        return room_key_list

    def dump_list(self, data_list, file_store):
        """Method to store a data list into a json file"""
        try:
            with open(file_store, "w", encoding="utf-8", newline="") as file:
                json.dump(data_list, file, indent=2)
        except FileNotFoundError as ex:
            raise HotelManagementException("Wrong file  or file path") from ex
    @classmethod
    def load_json_store(cls, file_store, message):
        """Method to load a json file"""
        # leo los datos del fichero , si no existe deber dar error porque el almacen de reservaa
        # debe existir para hacer el checkin
        try:
            with open(file_store, "r", encoding="utf-8", newline="") as file:
                store_list = json.load(file)
        except FileNotFoundError as ex:
            raise HotelManagementException(message) from ex
        except json.JSONDecodeError as ex:
            raise HotelManagementException("JSON Decode Error - Wrong JSON Format") from ex
        return store_list
