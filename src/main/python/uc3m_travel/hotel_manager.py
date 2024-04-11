"""Module for the hotel manager"""
import re
import json
from datetime import datetime
from src.main.python.uc3m_travel.hotel_management_exception import HotelManagementException
from src.main.python.uc3m_travel.hotel_reservation import HotelReservation
from src.main.python.uc3m_travel.hotel_stay import HotelStay
from src.main.python.uc3m_travel.hotel_management_config import JSON_FILES_PATH
from freezegun import freeze_time


class HotelManager:
    """Class with all the methods for managing reservations and stays"""
    def __init__(self):
        pass


    def validate_arrival_date(self, arrival_date):
        """validates the arrival date format  using regex"""
        myregex = re.compile(r"^(([0-2]\d|-3[0-1])\/(0\d|1[0-2])\/\d\d\d\d)$")
        res = myregex.fullmatch(arrival_date)
        if not res:
            raise HotelManagementException("Invalid date format")
        return arrival_date

    def validate_numdays(self,num_days):
        """validates the number of days"""
        try:
            days = int(num_days)
        except ValueError as ex:
            raise HotelManagementException("Invalid num_days datatype") from ex
        if (days < 1 or days > 10):
            raise HotelManagementException("Numdays should be in the range 1-10")
        return num_days


    @staticmethod
    def validate_dni_letter(dni):
        """RETURN TRUE IF THE DNI IS RIGHT, OR FALSE IN OTHER CASE"""
        letter_mapping = {"0": "T", "1": "R", "2": "W", "3": "A", "4": "G", "5": "M",
             "6": "Y", "7": "F", "8": "P", "9": "D", "10": "X", "11": "B",
             "12": "N", "13": "J", "14": "Z", "15": "S", "16": "Q", "17": "V",
             "18": "H", "19": "L", "20": "C", "21": "K", "22": "E"}
        din_digits = int(dni[0:8])
        remainder = str(din_digits % 23)
        return dni[8] == letter_mapping[remainder]

    def validate_dni(self, id_card):
        regex = r'^[0-9]{8}[A-Z]{1}$'
        my_regex = re.compile(regex)
        if not my_regex.fullmatch(id_card):
            raise HotelManagementException("Invalid IdCard format")
        if not self.validate_dni_letter(id_card):
            raise HotelManagementException("Invalid IdCard letter")
        return id_card

    def validate_localizer(self, localizer):
        """validates the localizer format using a regex"""
        regex = r'^[a-fA-F0-9]{32}$'
        myregex = re.compile(regex)
        if not myregex.fullmatch(localizer):
            raise HotelManagementException("Invalid localizer")
        return localizer

    def validate_roomkey(self, roomKey):
        """validates the roomkey format using a regex"""
        regex = r'^[a-fA-F0-9]{64}$'
        myregex = re.compile(regex)
        if not myregex.fullmatch(roomKey):
            raise HotelManagementException("Invalid room key format")
        return roomKey

    def validate_room_type(self, room_type):
        """validates the room type value using regex"""
        myregex = re.compile(r"(SINGLE|DOUBLE|SUITE)")
        res = myregex.fullmatch(room_type)
        if not res:
            raise HotelManagementException("Invalid roomtype value")
        return room_type

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
        if not self.validatecreditcard(creditCard):
            raise HotelManagementException("Invalid credit card number")
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

        # we validate these attributes using methods of this class because these attributes are present both in
        # HotelStay and HotelReservation, so we would be duplicating code if we moved the validate methods
        # to each class. However, for name_surname, credit card and phone number, since
        # those attribute only appear in HotelReservation, we move their validation methods to their class
        # and call them in the constructor
        room_type = self.validate_room_type(room_type)
        id_card = self.validate_dni(id_card)
        arrival_date = self.validate_arrival_date(arrival_date)
        num_days = self.validate_numdays(num_days)
        my_reservation = HotelReservation(id_card=id_card,
                                          credit_card_number=credit_card,
                                          name_surname=name_surname,
                                          phone_number=phone_number,
                                          room_type=room_type,
                                          arrival=arrival_date,
                                          num_days=num_days)

        # escribo el fichero Json con todos los datos
        file_store = JSON_FILES_PATH + "store_reservation.json"
        data_list = self.load_json_list(file_store)

        #compruebo que esta reserva no esta en la lista
        for item in data_list:
            if my_reservation.localizer == item["_HotelReservation__localizer"]:
                raise HotelManagementException ("Reservation already exists")
            if my_reservation.id_card == item["_HotelReservation__id_card"]:
                raise HotelManagementException("This ID card has another reservation")
        #añado los datos de mi reserva a la lista , a lo que hubiera
        data_list.append(my_reservation.__dict__)

        #escribo la lista en el fichero
        self.dump_list(data_list, file_store)

        return my_reservation.localizer

    def dump_list(self, data_list, file_store):
        try:
            with open(file_store, "w", encoding="utf-8", newline="") as file:
                json.dump(data_list, file, indent=2)
        except FileNotFoundError as ex:
            raise HotelManagementException("Wrong file  or file path") from ex

    def guest_arrival(self, file_input:str)->str:
        """manages the arrival of a guest with a reservation"""
        input_list = self.load_json_store(file_input, "Error: file input not found")

        # comprobar valores del fichero
        try:
            my_localizer = input_list["Localizer"]
            my_id_card = input_list["IdCard"]
        except KeyError as exception:
            raise HotelManagementException("Error - Invalid Key in JSON") from exception

        #validate idCcard and localizer
        self.validate_dni(my_id_card)
        self.validate_localizer(my_localizer)

        # look in reservation store
        file_store = JSON_FILES_PATH + "store_reservation.json"
        store_list = self.load_json_store(file_store, "Error: store reservation not found")

        # compruebo si esa reserva esta en el almacen
        found = False
        for item in store_list:
            if my_localizer == item["_HotelReservation__localizer"]:
                reservation_days = item["_HotelReservation__num_days"]
                reservation_room_type = item["_HotelReservation__room_type"]
                reservation_date_timestamp = item["_HotelReservation__reservation_date"]
                reservation_credit_card = item["_HotelReservation__credit_card_number"]
                reservation_date_arrival = item["_HotelReservation__arrival"]
                reservation_name = item["_HotelReservation__name_surname"]
                reservation_phone = item["_HotelReservation__phone_number"]
                reservation_id_card = item["_HotelReservation__id_card"]
                found = True

        if not found:
            raise HotelManagementException("Error: localizer not found")
        if my_id_card != reservation_id_card:
            raise HotelManagementException("Error: Localizer is not correct for this IdCard")

        # regenerate key and check if it matches
        reservation_date = datetime.fromtimestamp(reservation_date_timestamp)

        with freeze_time(reservation_date):
            new_reservation = HotelReservation(credit_card_number=reservation_credit_card,
                                               id_card=reservation_id_card,
                                               num_days=reservation_days,
                                               room_type=reservation_room_type,
                                               arrival=reservation_date_arrival,
                                               name_surname=reservation_name,
                                               phone_number=reservation_phone)
        if new_reservation.localizer != my_localizer:
            raise HotelManagementException("Error: reservation has been manipulated")

        # compruebo si hoy es la fecha de checkin
        reservation_format = "%d/%m/%Y"
        date_obj = datetime.strptime(reservation_date_arrival, reservation_format)
        if date_obj.date()!= datetime.date(datetime.utcnow()):
            raise HotelManagementException("Error: today is not reservation date")

        # genero la room key para ello llamo a Hotel Stay
        my_checkin = HotelStay(idcard=my_id_card, numdays=int(reservation_days),
                               localizer=my_localizer, roomtype=reservation_room_type)

        #Ahora lo guardo en el almacen nuevo de checkin
        # escribo el fichero Json con todos los datos
        file_store = JSON_FILES_PATH + "store_check_in.json"

        room_key_list = self.load_json_list(file_store)

        # comprobar que no he hecho otro ckeckin antes
        for item in room_key_list:
            if my_checkin.room_key == item["_HotelStay__room_key"]:
                raise HotelManagementException ("ckeckin  ya realizado")

        #añado los datos de mi reserva a la lista , a lo que hubiera
        room_key_list.append(my_checkin.__dict__)

        self.dump_list(room_key_list, file_store)

        return my_checkin.room_key

    def load_json_store(self, file_store, message):
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

    def load_json_list(self, file_store):
        # leo los datos del fichero si existe , y si no existe creo una lista vacia
        try:
            with open(file_store, "r", encoding="utf-8", newline="") as file:
                room_key_list = json.load(file)
        except FileNotFoundError as ex:
            room_key_list = []
        except json.JSONDecodeError as ex:
            raise HotelManagementException("JSON Decode Error - Wrong JSON Format") from ex
        return room_key_list


    def guest_checkout(self, room_key:str)->bool:
        """manages the checkout of a guest"""
        self.validate_roomkey(room_key)

        #check that the roomkey is stored in the checkins file
        file_store = JSON_FILES_PATH + "store_check_in.json"
        room_key_list = self.load_json_store(file_store, "Error: store checkin not found")

        # comprobar que esa room_key es la que me han dado
        found = False
        for item in room_key_list:
            if room_key == item["_HotelStay__room_key"]:
                departure_date_timestamp = item["_HotelStay__departure"]
                found = True
        if not found:
            raise HotelManagementException ("Error: room key not found")

        today = datetime.utcnow().date()
        if datetime.fromtimestamp(departure_date_timestamp).date() != today:
            raise HotelManagementException("Error: today is not the departure day")


        file_store_checkout = JSON_FILES_PATH + "store_check_out.json"
        room_key_list = self.load_json_list(file_store_checkout)

        for checkout in room_key_list:
            if checkout["room_key"] == room_key:
                raise HotelManagementException("Guest is already out")

        room_checkout={"room_key":  room_key, "checkout_time":datetime.timestamp(datetime.utcnow())}

        room_key_list.append(room_checkout)

        self.dump_list(room_key_list, file_store_checkout)

        return True
