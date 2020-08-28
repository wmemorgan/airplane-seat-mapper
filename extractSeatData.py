import xml.etree.ElementTree as ET

tree = ET.parse("OTA_AirSeatMapRS.xml")
data = tree.getroot()
print(data)
root = tree.findall(
    './/{http://www.opentravel.org/OTA/2003/05/common/}SeatInfo')
print(len(root))
seatInfo = []
# seatInfo = {}
for i in range(5, 15):
    seat = {}
    for node in root[i].iter():

        if "SeatInfo" in node.tag:
            if node.get('BulkheadInd') == "true":
                seat.update({
                    "rowtype": "Bulkhead"
                })
            elif node.get('ExitRowInd') == "true":
                seat.update({
                    "rowtype": "Exit"
                })
            else:
                seat.update({
                    "rowtype": "Standard"
                })

            seat.update({
                "planesection": node.get('PlaneSection')
            })

        if "Summary" in node.tag:
            row = int(node.get('SeatNumber')[0])
            if (row < 7):
                seat.update({"cabinclass": "First"})
            else:
                seat.update({"cabinclass": "Economy"})

            seat.update({
                "seatnumber": node.get('SeatNumber'),
                "available": bool(node.get('AvailableInd')=="true")
            })

        if "Features" in node.tag:
            if node.text in ['Aisle', 'Center', 'Window']:
                seat.update({
                    "location": node.text
                })

            isPreferred = bool(node.get('extension') == "Preferred")
            seat.update({
                "preferred": True if isPreferred else False
            })

            byBathroom = bool(node.get('extension') == "Lavatory")
            seat.update({
                "bathroom": True if byBathroom else False
            })

        if "Fee" in node.tag:
            seat.update({
                "price": int(node.attrib.get('Amount'))
            })
        else:
            seat.update({
                "price": 0
            })
    # seatInfo.update({f"Record{i}": seat})
    seatInfo.append(seat)

print(seatInfo)
