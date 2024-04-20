from src.main.python.uc3m_travel import HotelManager
from src.main.python.uc3m_travel.storage.checkout_json_store import CheckoutJsonStore
from src.main.python.uc3m_travel.storage.reservation_json_store import ReservationJsonStore
from src.main.python.uc3m_travel.storage.stay_json_store import StayJsonStore
from src.main.python.uc3m_travel.attributes.attribute_room_type import RoomType
from unittest import TestCase


class MyTestCase(TestCase):
    def test_singleton_hotel_manager(self):
        hotel_manager_1 = HotelManager()
        hotel_manager_2 = HotelManager()
        hotel_manager_3 = HotelManager()

        self.assertEqual(hotel_manager_1, hotel_manager_2)
        self.assertEqual(hotel_manager_2, hotel_manager_3)
        self.assertEqual(hotel_manager_3, hotel_manager_1)

    def test_singleton_CheckoutJsonStore(self):
        CheckoutJsonStore_1 = CheckoutJsonStore()
        CheckoutJsonStore_2 = CheckoutJsonStore()
        CheckoutJsonStore_3 = CheckoutJsonStore()

        self.assertEqual(CheckoutJsonStore_1, CheckoutJsonStore_2)
        self.assertEqual(CheckoutJsonStore_1, CheckoutJsonStore_3)
        self.assertEqual(CheckoutJsonStore_2, CheckoutJsonStore_3)

    def test_singleton_ReservationJsonStore(self):
        ReservationJsonStore_1 = ReservationJsonStore()
        ReservationJsonStore_2 = ReservationJsonStore()
        ReservationJsonStore_3 = ReservationJsonStore()

        self.assertEqual(ReservationJsonStore_1, ReservationJsonStore_2)
        self.assertEqual(ReservationJsonStore_1, ReservationJsonStore_3)
        self.assertEqual(ReservationJsonStore_2, ReservationJsonStore_3)

    def test_singleton_StayJsonStore(self):
        StayJsonStore_1 = StayJsonStore()
        StayJsonStore_2 = StayJsonStore()
        StayJsonStore_3 = StayJsonStore()

        self.assertEqual(StayJsonStore_1, StayJsonStore_2)
        self.assertEqual(StayJsonStore_1, StayJsonStore_3)
        self.assertEqual(StayJsonStore_2, StayJsonStore_3)

    def test_class_with_no_singleton(self):
        roomType_1 = RoomType("SINGLE")
        roomType_2 = RoomType("SINGLE")
        self.assertNotEqual(roomType_1, roomType_2)