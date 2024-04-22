from src.main.python.uc3m_travel.storage.json_store import JsonStore
from src.main.python.uc3m_travel.hotel_management_config import JSON_FILES_PATH
from src.main.python.uc3m_travel.hotel_management_exception import HotelManagementException


class ReservationJsonStore(JsonStore):
    """Class that contains the methods related to json files in room_reservation"""
    class __ReservationJsonStore(JsonStore):
        def __init__(self):
            pass
        """ReservationJsonStore singleton class"""
        def save_reservation(self, my_reservation):
            """Method that saves the reservation in the store_reservation file"""
            file_store = JSON_FILES_PATH + "store_reservation.json"
            data_list = self.load_json_list(file_store)
            # compruebo que esta reserva no esta en la lista
            for item in data_list:
                if my_reservation.localizer == item["_HotelReservation__localizer"]:
                    raise HotelManagementException("Reservation already exists")
                if my_reservation.id_card == item["_HotelReservation__id_card"]:
                    raise HotelManagementException("This ID card has another reservation")
            # añado los datos de mi reserva a la lista , a lo que hubiera
            data_list.append(my_reservation.__dict__)
            # escribo la lista en el fichero
            self.dump_list(data_list, file_store)

    __instance = None
    def __new__(cls):
        if not ReservationJsonStore.__instance:
            ReservationJsonStore.__instance = ReservationJsonStore.__ReservationJsonStore()
        return ReservationJsonStore.__instance
