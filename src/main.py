"""Convert XML Seat Data to JSON

This script extracts seat data from an OTA airline booking system
file and outputs it to JSON format.

This tool accepts OTA xml files (.xml).

This script imports the following functions:
    * get_seat_data - to extract and shape seat data
    * create_json_file - outputs the seat data to a JSON file

This file can also be imported as a module and contains the following
functions:

    * main - the main function of the script
"""

from getSeatData import get_seat_data
from fileUtilities import create_json_file

def main():
    seat_info = get_seat_data()
    create_json_file(seat_info, "seatinfo.json")

if __name__ == "__main__":
    main()

