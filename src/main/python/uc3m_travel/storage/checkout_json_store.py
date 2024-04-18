from src.main.python.uc3m_travel.storage.json_store import JsonStore
from src.main.python.uc3m_travel.hotel_management_config import JSON_FILES_PATH
from src.main.python.uc3m_travel.hotel_management_exception import HotelManagementException
from datetime import datetime


class CheckoutJsonStore(JsonStore):

    @classmethod
    def find_roomkey(cls, room_key):
        file_store = JSON_FILES_PATH + "store_check_in.json"
        room_key_list = JsonStore.load_json_store(file_store, "Error: store checkin not found")
        # comprobar que esa room_key es la que me han dado
        found = False
        for item in room_key_list:
            if room_key == item["_HotelStay__room_key"]:
                departure_date_timestamp = item["_HotelStay__departure"]
                found = True
        if not found:
            raise HotelManagementException("Error: room key not found")
        today = datetime.utcnow().date()
        if datetime.fromtimestamp(departure_date_timestamp).date() != today:
            raise HotelManagementException("Error: today is not the departure day")


    def save_checkout(self, room_key):
        file_store_checkout = JSON_FILES_PATH + "store_check_out.json"
        room_key_list = self.load_json_list(file_store_checkout)
        for checkout in room_key_list:
            if checkout["room_key"] == room_key:
                raise HotelManagementException("Guest is already out")
        room_checkout = {"room_key": room_key,
                         "checkout_time": datetime.timestamp(datetime.utcnow())}
        room_key_list.append(room_checkout)
        self.dump_list(room_key_list, file_store_checkout)
