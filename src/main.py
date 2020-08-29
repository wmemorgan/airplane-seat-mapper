"""Convert XML Seat Data to JSON

This script extracts seat data from an OTA airline booking system
file and outputs it to JSON format.

This tool accepts OTA xml files (.xml).

This script imports the 'getSeatData' module to extract
and shape seat data.

This file can also be imported as a module and contains the following
functions:

    * read_xml_file - reads the OTA xml file
    * create_json_file - outputs the seat data to a JSON file
    * main - the main function of the script
"""

import xml.etree.ElementTree as ET
import json
from getSeatData import get_seat_data

def read_xml_file(input_file, elem):
    """Reads xml data and extracts specified elements
    
    Parameters
    ----------
    input_file : str
        The OTA xml file
    elem : str
        Specified elements to be extracted

    Returns
    -------
    list
        a list of xml seat data
    """
    tree = ET.parse(input_file)
    root = tree.findall(elem)

    return root

def create_json_file(data, output_file):
    json_data = json.dumps(data)

    with open(f"../output/{output_file}", "w") as json_file:
        json_file.write(json_data)
        json_file.close()

def main():
    tree = ET.parse("OTA_AirSeatMapRS.xml")
    seat_data = read_xml_file("OTA_AirSeatMapRS.xml",
                          './/{http://www.opentravel.org/OTA/2003/05/common/}SeatInfo')  
    row_data = read_xml_file("OTA_AirSeatMapRS.xml",
                          './/{http://www.opentravel.org/OTA/2003/05/common/}RowInfo')  
    seat_info = get_seat_data(seat_data, row_data)
    print(seat_info)
    create_json_file(seat_info, "seatinfo.json")

if __name__ == "__main__":
    main()

