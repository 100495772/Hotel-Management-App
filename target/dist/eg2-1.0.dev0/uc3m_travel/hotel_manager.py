"""Module for the hotel manager"""
import json
from src.main.python.uc3m_travel.hotel_management_exception import HotelManagementException
from src.main.python.uc3m_travel.hotel_reservation import HotelReservation
from src.main.python.uc3m_travel.hotel_stay import HotelStay
from src.main.python.uc3m_travel.attributes.attribute_id_card import IdCard
from src.main.python.uc3m_travel.attributes.attribute_room_type import RoomType
from src.main.python.uc3m_travel.attributes.attribute_arrivaldate import ArrivalDate
from src.main.python.uc3m_travel.attributes.attribute_room_key import RoomKey
from src.main.python.uc3m_travel.storage.reservation_json_store import ReservationJsonStore
from src.main.python.uc3m_travel.storage.stay_json_store import StayJsonStore
from src.main.python.uc3m_travel.storage.checkout_json_store import CheckoutJsonStore


class HotelManager:
    """Class with all the methods for managing reservations and stays"""
    class __HotelManager:
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
                raise HotelManagementException("JSON Decode Error - "
                                               "Wrong JSON Format") from exception
            try:
                credit_card = json_data["CreditCard"]
                phone_number = json_data["phoneNumber"]
                req = HotelReservation(id_card="12345678Z",
                                       credit_card_number=credit_card,
                                       name_surname="John Doe",
                                       phone_number=phone_number,
                                       room_type="single",
                                       num_days=3,
                                       arrival="20/01/2024")
            except KeyError as exception:
                raise HotelManagementException("JSON Decode Error -"
                                               " Invalid JSON Key") from exception
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
            """ Manages the hotel reservation: creates a reservation
             and saves it into a json file"""

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
            my_checkin = HotelStay.create_guest_arrival_from_file(file_input)
            # Save the stay in the stay store
            stay_store = StayJsonStore()
            stay_store.save_stay(my_checkin)

            return my_checkin.room_key

        def guest_checkout(self, room_key:str)->bool:
            """manages the checkout of a guest"""
            room_key = str(RoomKey(room_key))

            #check that the roomkey is stored in the checkins file
            my_checkout = CheckoutJsonStore()
            my_checkout.find_roomkey(room_key)

            # Save the checkout in the checkout store
            checkout_store = CheckoutJsonStore()
            checkout_store.save_checkout(room_key)
            # CheckoutJsonStore.save_checkout(room_key)

            return True
    __instance = None

    def __new__(cls):
        if not HotelManager.__instance:
            HotelManager.__instance = HotelManager.__HotelManager()
        return HotelManager.__instance

    def __getattr__(self, item):
        return getattr(HotelManager().__instance, item)

    def __setattr__(self, key, value):
        return setattr(HotelManager().__instance, key, value)
