from src.main.python.uc3m_travel.storage.json_store import JsonStore
from src.main.python.uc3m_travel.hotel_management_config import JSON_FILES_PATH
from src.main.python.uc3m_travel.hotel_management_exception import HotelManagementException


class ReservationJsonStore(JsonStore):
    """ReservationJsonStore singleton class"""

    _file_name = JSON_FILES_PATH + "store_reservation.json"

    def save_reservation(self, my_reservation):
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
