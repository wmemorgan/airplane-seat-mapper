"""Get Seat Data

This script parses seat information from the OTA xml extract. 

This file can also be imported as a module and contains the following
functions:
    * get_seat_data - returns seat data
"""
import xml.etree.ElementTree as ET

tree = ET.parse("OTA_AirSeatMapRS.xml")


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

    seat_data = tree.findall(
        './/{http://www.opentravel.org/OTA/2003/05/common/}SeatInfo')

    row_data = tree.findall(
        './/{http://www.opentravel.org/OTA/2003/05/common/}RowInfo')
    # Extract row attributes for seat class identification
    rowList = []
    for elem in row_data:
        rowList.append(elem.attrib)

    # Extract seat attributes
    seatlist = []
    for seat in seat_data:
        seatItem = {}
        
        if seat.attrib["BulkheadInd"] == "true":
            seatItem.update({"row_type": "Bulkhead"})
        elif seat.attrib["ExitRowInd"] == "true":
            seatItem.update({"row_type": "Exit"})
        else:
            seatItem.update({"row_type": "Standard"})

        seatItem["planesection"] = seat.get("PlaneSection")

        summary = seat.findall(
            './/{http://www.opentravel.org/OTA/2003/05/common/}Summary')
        for item in summary:
            rowNumber = item.attrib["SeatNumber"][:-1]
            cabin_class = next((row['CabinType']
                                for row in rowList if row['RowNumber'] == rowNumber), None)
            seatItem.update(
                {
                    "class": cabin_class,
                    "seatnumber": item.attrib["SeatNumber"], 
                    "isavailable": bool(item.attrib["AvailableInd"] == "true") 
                })

        features = seat.findall(
            './/{http://www.opentravel.org/OTA/2003/05/common/}Features')
        for feature in features:
            if feature.text in ['Aisle', 'Center', 'Window']:
                seatItem["location"] = feature.text

            if feature.get("extension"):
                isPreferred = bool(feature.get('extension') == "Preferred")
                if isPreferred:
                    seatItem["ispreferred"] = True
                byBathroom = bool(feature.get('extension') == "Lavatory")
                if byBathroom:
                    seatItem["isbathroom"] = True
        
        if "ispreferred" not in seatItem:
            seatItem["ispreferred"] = False
        if "isbathroom" not in seatItem:
            seatItem["isbathroom"] = True

        fees = seat.findall(
            './/{http://www.opentravel.org/OTA/2003/05/common/}Fee')
        if len(fees) > 0:           
            for fee in fees:
                if fee.get("Amount"):
                    seatItem["price"] = int(fee.get("Amount"))
        elif len(fees) == 0:
            seatItem["price"] = 0

        seatlist.append(seatItem)
    return seatlist
