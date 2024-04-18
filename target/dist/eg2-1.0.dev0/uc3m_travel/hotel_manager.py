"""Module for the hotel manager"""
import re
import json
from datetime import datetime
from freezegun import freeze_time

from src.main.python.uc3m_travel.hotel_management_exception import HotelManagementException
from src.main.python.uc3m_travel.hotel_reservation import HotelReservation
from src.main.python.uc3m_travel.hotel_stay import HotelStay
from src.main.python.uc3m_travel.hotel_management_config import JSON_FILES_PATH
from src.main.python.uc3m_travel.attributes.attribute_id_card import IdCard
from src.main.python.uc3m_travel.attributes.attribute_room_type import RoomType
from src.main.python.uc3m_travel.attributes.attribute_arrivaldate import ArrivalDate
from src.main.python.uc3m_travel.attributes.attribute_localizer import Localizer
from src.main.python.uc3m_travel.attributes.attribute_room_key import RoomKey
from src.main.python.uc3m_travel.storage.json_store import JsonStore
from src.main.python.uc3m_travel.storage.reservation_json_store import ReservationJsonStore
from src.main.python.uc3m_travel.storage.stay_json_store import StayJsonStore
from src.main.python.uc3m_travel.storage.checkout_json_store import CheckoutJsonStore


class HotelManager:
    """Class with all the methods for managing reservations and stays"""
    def __init__(self):
        pass

    def validate_numdays(self,num_days):
        """validates the number of days"""
        try:
            days = int(num_days)
        except ValueError as ex:
            raise HotelManagementException("Invalid num_days datatype") from ex
        if (days < 1 or days > 10):
            raise HotelManagementException("Numdays should be in the range 1-10")
        return num_days


    def read_data_from_json(self, file):
        """reads the content of a json file with two fields: CreditCard and phoneNumber"""
        try:
            with open(file, encoding='utf-8') as input_file:
                json_data = json.load(input_file)
        except FileNotFoundError as exception:
            raise HotelManagementException("Wrong file or file path") from exception
        except json.JSONDecodeError as exception:
            raise HotelManagementException("JSON Decode Error - Wrong JSON Format") from exception
        try:
            creditCard = json_data["CreditCard"]
            phoneNumber = json_data["phoneNumber"]
            req = HotelReservation(id_card="12345678Z",
                                   credit_card_number=creditCard,
                                   name_surname="John Doe",
                                   phone_number=phoneNumber,
                                   room_type="single",
                                   num_days=3,
                                   arrival="20/01/2024")
        except KeyError as exception:
            raise HotelManagementException("JSON Decode Error - Invalid JSON Key") from exception
        #if not self.validatecreditcard(creditCard):
            #raise HotelManagementException("Invalid credit card number")
        # Close the file
        return req

    # pylint: disable=too-many-arguments
    def room_reservation(self,
                         credit_card:str,
                         name_surname:str,
                         id_card:str,
                         phone_number:str,
                         room_type:str,
                         arrival_date: str,
                         num_days:int)->str:
        """ Manages the hotel reservation: creates a reservation and saves it into a json file"""

        # we use the extracted attribute classes to validate
        room_type = str(RoomType(room_type))
        id_card = str(IdCard(id_card))
        arrival_date = str(ArrivalDate(arrival_date))
        num_days = self.validate_numdays(num_days)
        my_reservation = HotelReservation(id_card=id_card,
                                          credit_card_number=credit_card,
                                          name_surname=name_surname,
                                          phone_number=phone_number,
                                          room_type=room_type,
                                          arrival=arrival_date,
                                          num_days=num_days)

        reservation_store = ReservationJsonStore()
        # escribo el fichero Json con todos los datos
        reservation_store.save_reservation(my_reservation)

        return my_reservation.localizer

    def guest_arrival(self, file_input:str)->str:
        """manages the arrival of a guest with a reservation"""
        input_list = JsonStore.load_json_store(file_input, "Error: file input not found")

        # comprobar valores del fichero
        try:
            my_localizer = input_list["Localizer"]
            my_id_card = input_list["IdCard"]
        except KeyError as exception:
            raise HotelManagementException("Error - Invalid Key in JSON") from exception

        #validate idCcard and localizer using extracted classes
        my_id_card = str(IdCard(my_id_card))
        my_localizer = str(Localizer(my_localizer))

        reservation_data = StayJsonStore.find_reservation(my_id_card, my_localizer)

        # regenerate key and check if it matches
        reservation_date = datetime.fromtimestamp(reservation_data["_HotelReservation__reservation_date"])

        with freeze_time(reservation_date):
            new_reservation = HotelReservation(credit_card_number=reservation_data["_HotelReservation__credit_card_number"],
                                               id_card=reservation_data["_HotelReservation__id_card"],
                                               num_days=reservation_data["_HotelReservation__num_days"],
                                               room_type=reservation_data["_HotelReservation__room_type"],
                                               arrival=reservation_data["_HotelReservation__arrival"],
                                               name_surname=reservation_data["_HotelReservation__name_surname"],
                                               phone_number=reservation_data["_HotelReservation__phone_number"])
        if new_reservation.localizer != my_localizer:
            raise HotelManagementException("Error: reservation has been manipulated")

        # compruebo si hoy es la fecha de checkin
        reservation_format = "%d/%m/%Y"
        date_obj = datetime.strptime(reservation_data["_HotelReservation__arrival"], reservation_format)
        if date_obj.date()!= datetime.date(datetime.utcnow()):
            raise HotelManagementException("Error: today is not reservation date")

        # genero la room key para ello llamo a Hotel Stay
        my_checkin = HotelStay(idcard=my_id_card, numdays=int(reservation_data["_HotelReservation__num_days"]),
                               localizer=my_localizer, roomtype=reservation_data["_HotelReservation__room_type"])

        # Save the stay in the stay store
        stay_store = StayJsonStore()
        stay_store.save_stay(my_checkin)

        return my_checkin.room_key


    def guest_checkout(self, room_key:str)->bool:
        """manages the checkout of a guest"""
        room_key = str(RoomKey(room_key))

        #check that the roomkey is stored in the checkins file
        CheckoutJsonStore.find_roomkey(room_key)

        # Save the checkout in the checkout store
        checkout_store = CheckoutJsonStore()
        checkout_store.save_checkout(room_key)

        return True
