"""Get Seat Data

This script parses seat information from the OTA xml extract. 

This script imports the following functions:
    * read_xml_file - returns list of elements

This file can also be imported as a module and contains the following
functions:

    * get_seat_data - returns seat data
"""

from fileUtilities import read_xml_file

def get_seat_data():
    """ Gets seat data from xml extract

    Parameters
    ----------
    seatdata : list
        Extract seat data from OTA xml file
    rowdata : list
        Extract plane row data from OTA xml file
    seatlist: list, optional
        List of dictionaries containing seat information
    """

    seat_data = read_xml_file("OTA_AirSeatMapRS.xml",
                              './/{http://www.opentravel.org/OTA/2003/05/common/}SeatInfo')
    row_data = read_xml_file("OTA_AirSeatMapRS.xml",
                             './/{http://www.opentravel.org/OTA/2003/05/common/}RowInfo')

    # Extract row attributes for seat class identification
    rowList = []
    for elem in row_data:
        rowList.append(elem.attrib)

    # Extract seat attributes
    seatlist = []
    for elem in seat_data:
        # Store individual seat data
        seat = {}
        # Extract seat specific data
        for node in elem.iter():
            if "SeatInfo" in node.tag:
                if node.get('BulkheadInd') == "true":
                    seat.update({"rowtype": "Bulkhead"})

                elif node.get('ExitRowInd') == "true":
                    seat.update({"rowtype": "Exit"})

                else:
                    seat.update({"rowtype": "Standard"})

                seat.update({"planesection": node.get('PlaneSection')})

            if "Summary" in node.tag:
                # Use row data to identify cabin class
                rowNumber = node.get('SeatNumber')[:-1]
                cabin_class = next((row['CabinType']
                                    for row in rowList if row['RowNumber'] == rowNumber), None)
                isavailable = bool(node.get('AvailableInd') == "true")

                seat.update({
                    "class": cabin_class,
                    "seatnumber": node.get('SeatNumber'),
                    "isavailable": isavailable
                })

                if isavailable == False:
                    # Displays '0' amount if seat is unavailable
                    seat.update({"price": 0})

            if "Features" in node.tag:
                if node.text in ['Aisle', 'Center', 'Window']:
                    seat.update({"location": node.text})

                isPreferred = bool(node.get('extension') == "Preferred")
                seat.update({"ispreferred": True if isPreferred else False})

                byBathroom = bool(node.get('extension') == "Lavatory")
                seat.update({"isbathroom": True if byBathroom else False})

            if "Fee" in node.tag:
                seat.update({"price": int(node.attrib.get('Amount'))})

        seatlist.append(seat)
    return seatlist
