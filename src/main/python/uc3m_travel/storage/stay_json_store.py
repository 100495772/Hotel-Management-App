from src.main.python.uc3m_travel.storage.json_store import JsonStore
from src.main.python.uc3m_travel.hotel_management_config import JSON_FILES_PATH
from src.main.python.uc3m_travel.hotel_management_exception import HotelManagementException


class StayJsonStore(JsonStore):
    """Class that contains the methods related to json files in guest_arrival"""
    class __StayJsonStore(JsonStore):
        def __init__(self):
            pass
        @classmethod
        def find_reservation(cls, my_id_card, my_localizer):
            """Method that finds the reservation that contains my_id_card and my_localizer"""
            # look in reservation store
            file_store = JSON_FILES_PATH + "store_reservation.json"
            store_list = JsonStore.load_json_store(file_store, "Error: store reservation not found")
            # compruebo si esa reserva esta en el almacen
            found = False
            for item in store_list:
                if my_localizer == item["_HotelReservation__localizer"]:
                    reservation_id_card = item["_HotelReservation__id_card"]
                    found = True
                    result = item
            if not found:
                raise HotelManagementException("Error: localizer not found")
            if my_id_card != reservation_id_card:
                raise HotelManagementException("Error: Localizer is not correct for this IdCard")
            return result

        def save_stay(self, my_checkin):
            """Method that saves the stay in the store_check_in file"""
            # Ahora lo guardo en el almacen nuevo de checkin
            # escribo el fichero Json con todos los datos
            file_store = JSON_FILES_PATH + "store_check_in.json"
            room_key_list = self.load_json_list(file_store)
            # comprobar que no he hecho otro ckeckin antes
            for item in room_key_list:
                if my_checkin.room_key == item["_HotelStay__room_key"]:
                    raise HotelManagementException("ckeckin  ya realizado")
            # añado los datos de mi reserva a la lista , a lo que hubiera
            room_key_list.append(my_checkin.__dict__)
            self.dump_list(room_key_list, file_store)

    __instance = None

    def __new__(cls):
        if not StayJsonStore.__instance:
            StayJsonStore.__instance = StayJsonStore.__StayJsonStore()
        return StayJsonStore.__instance
