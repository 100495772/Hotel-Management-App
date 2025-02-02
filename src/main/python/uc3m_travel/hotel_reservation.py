"""Hotel reservation class"""
import hashlib
from datetime import datetime
from freezegun import freeze_time
from src.main.python.uc3m_travel.attributes.attribute_phone_number import PhoneNumber
from src.main.python.uc3m_travel.attributes.attribute_name_surname import Name
from src.main.python.uc3m_travel.attributes.attribute_credit_card import CreditCard
from src.main.python.uc3m_travel.attributes.attribute_id_card import IdCard
from src.main.python.uc3m_travel.attributes.attribute_localizer import Localizer
from src.main.python.uc3m_travel.storage.stay_json_store import StayJsonStore
from src.main.python.uc3m_travel.hotel_management_exception import HotelManagementException


class HotelReservation:
    """Class for representing hotel reservations"""
    #pylint: disable=too-many-arguments, too-many-instance-attributes
    def __init__(self,
                 id_card:str,
                 credit_card_number:str,
                 name_surname:str,
                 phone_number:str,
                 room_type:str,
                 arrival:str,
                 num_days:int):
        """constructor of reservation objects"""
        self.__credit_card_number = CreditCard(credit_card_number).value
        self.__id_card = id_card
        justnow = datetime.utcnow()
        self.__arrival = arrival
        self.__reservation_date = datetime.timestamp(justnow)
        self.__name_surname = Name(name_surname).value
        self.__phone_number = PhoneNumber(phone_number).value
        self.__room_type = room_type
        self.__num_days = num_days
        self.__localizer = hashlib.md5(str(self).encode()).hexdigest()

    def __str__(self):
        """return a json string with the elements required to calculate the localizer"""
        #VERY IMPORTANT: JSON KEYS CANNOT BE RENAMED
        json_info = {"id_card": self.__id_card,
                     "name_surname": self.__name_surname,
                     "credit_card": self.__credit_card_number,
                     "phone_number:": self.__phone_number,
                     "reservation_date": self.__reservation_date,
                     "arrival_date": self.__arrival,
                     "num_days": self.__num_days,
                     "room_type": self.__room_type,
                     }
        return "HotelReservation:" + json_info.__str__()
    @property
    def credit_card(self):
        """property for getting and setting the credit_card number"""
        return self.__credit_card_number
    @credit_card.setter
    def credit_card(self, value):
        self.__credit_card_number = value

    @property
    def id_card(self):
        """property for getting and setting the id_card"""
        return self.__id_card
    @id_card.setter
    def id_card(self, value):
        self.__id_card = value

    @property
    def arrival(self):
        """property for getting and setting the arrival date"""
        return self.__arrival
    @property
    def num_days(self):
        """property for getting and setting the number of days"""
        return self.__num_days

    @property
    def room_type(self):
        """property for getting and setting the room_type"""
        return self.__room_type

    @property
    def localizer(self):
        """Returns the md5 signature"""
        return self.__localizer


    @classmethod
    def create_reservation_from_arrival(cls, my_id_card, my_localizer):
        """Method that creates a reservation object from a valid id card and localizer"""
        my_id_card = IdCard(my_id_card).value
        my_localizer = Localizer(my_localizer).value
        reservations_store = StayJsonStore()
        reservation = reservations_store.find_reservation(my_id_card, my_localizer)
        if reservation is None:
            raise HotelManagementException("Error: localizer not found")
        if my_id_card != reservation["_HotelReservation__id_card"]:
            raise HotelManagementException("Error: Localizer is not correct for this IdCard")
        # regenrar clave y ver si coincide
        reservation_date = datetime.fromtimestamp(
            reservation["_HotelReservation__reservation_date"])
        with freeze_time(reservation_date):
            new_reservation = cls(
                credit_card_number=reservation["_HotelReservation__credit_card_number"],
                              id_card=reservation["_HotelReservation__id_card"],
                              num_days=reservation["_HotelReservation__num_days"],
                                room_type = reservation["_HotelReservation__room_type"],
                                arrival = reservation["_HotelReservation__arrival"],
                                name_surname = reservation["_HotelReservation__name_surname"],
                                phone_number = reservation["_HotelReservation__phone_number"])
            if new_reservation.localizer != my_localizer:
                raise HotelManagementException("Error: reservation has been manipulated")
        return new_reservation
