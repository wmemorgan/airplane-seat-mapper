import os
import unittest
from getSeatData import get_seat_data
from fileUtilities import read_xml_file, create_json_file

class SeatDataTests(unittest.TestCase):
    def setUp(self):
        self.seats = read_xml_file("OTA_AirSeatMapRS.xml",
                                   './/{http://www.opentravel.org/OTA/2003/05/common/}SeatInfo')
        self.rows = read_xml_file("OTA_AirSeatMapRS.xml",
                                  './/{http://www.opentravel.org/OTA/2003/05/common/}RowInfo')
        self.seat_data = get_seat_data()

    def test_read_xml_file(self):
        seats = read_xml_file("OTA_AirSeatMapRS.xml",
                                   './/{http://www.opentravel.org/OTA/2003/05/common/}SeatInfo')
        rows = read_xml_file("OTA_AirSeatMapRS.xml",
                                  './/{http://www.opentravel.org/OTA/2003/05/common/}RowInfo')
        self.assertEqual(len(seats), 170)
        self.assertEqual(len(rows), 29)

    def test_get_seat_data(self):
        test_data = get_seat_data()
        self.assertEqual(len(test_data), len(self.seats))

    def test_create_json_file(self):
        test_data = get_seat_data()
        create_json_file(test_data, "test-data.json")
        assert os.path.exists("../output/test-data.json")
        os.remove("../output/test-data.json")

    def test_cabin_class(self):
        for seat in self.seat_data:
            if int(seat["seatnumber"][:-1]) > 6:
                self.assertTrue(seat["class"] == "Economy")
            else:
                self.assertTrue(seat["class"] == "First")
    
    def test_price_data(self):
        for seat in self.seat_data:
            if seat["isavailable"]:
                self.assertTrue(seat["price"] > 0)
            else:
                self.assertTrue(seat["price"] == 0)



if __name__ == '__main__':
  unittest.main()


