from unittest import TestCase
from src.main.python.uc3m_travel import HotelManager
from src.main.python.uc3m_travel.storage.checkout_json_store import CheckoutJsonStore
from src.main.python.uc3m_travel.storage.reservation_json_store import ReservationJsonStore
from src.main.python.uc3m_travel.storage.stay_json_store import StayJsonStore
from src.main.python.uc3m_travel.attributes.attribute_room_type import RoomType


class MyTestCase(TestCase):
    def test_singleton_hotel_manager(self):
        hotel_manager_1 = HotelManager()
        hotel_manager_2 = HotelManager()
        hotel_manager_3 = HotelManager()

        self.assertEqual(hotel_manager_1, hotel_manager_2)
        self.assertEqual(hotel_manager_2, hotel_manager_3)
        self.assertEqual(hotel_manager_3, hotel_manager_1)

    def test_singleton_CheckoutJsonStore(self):
        checkout_json_store_1 = CheckoutJsonStore()
        checkout_json_store_2 = CheckoutJsonStore()
        checkout_json_store_3 = CheckoutJsonStore()

        self.assertEqual(checkout_json_store_1, checkout_json_store_2)
        self.assertEqual(checkout_json_store_1, checkout_json_store_3)
        self.assertEqual(checkout_json_store_2, checkout_json_store_3)

    def test_singleton_ReservationJsonStore(self):
        reservation_json_store_1 = ReservationJsonStore()
        reservation_json_store_2 = ReservationJsonStore()
        reservation_json_store_3 = ReservationJsonStore()

        self.assertEqual(reservation_json_store_1, reservation_json_store_2)
        self.assertEqual(reservation_json_store_1, reservation_json_store_3)
        self.assertEqual(reservation_json_store_2, reservation_json_store_3)

    def test_singleton_StayJsonStore(self):
        stay_json_store_1 = StayJsonStore()
        stay_json_store_2 = StayJsonStore()
        stay_json_store_3 = StayJsonStore()

        self.assertEqual(stay_json_store_1, stay_json_store_2)
        self.assertEqual(stay_json_store_1, stay_json_store_3)
        self.assertEqual(stay_json_store_2, stay_json_store_3)

    def test_class_with_no_singleton(self):
        room_type_1 = RoomType("SINGLE")
        room_type_2 = RoomType("SINGLE")
        self.assertNotEqual(room_type_1, room_type_2)
