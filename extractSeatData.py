import xml.etree.ElementTree as ET
import json

tree = ET.parse("OTA_AirSeatMapRS.xml")
root = tree.findall(
    './/{http://www.opentravel.org/OTA/2003/05/common/}SeatInfo')

seatInfo = []
# seatInfo = {}
for i in range(5, 12):
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
                seat.update({"class": "First"})
            else:
                seat.update({"class": "Economy"})

            seat.update({
                "seatnumber": node.get('SeatNumber'),
                "isavailable": bool(node.get('AvailableInd')=="true")
            })

        if "Features" in node.tag:
            if node.text in ['Aisle', 'Center', 'Window']:
                seat.update({
                    "location": node.text
                })

            isPreferred = bool(node.get('extension') == "Preferred")
            seat.update({
                "ispreferred": True if isPreferred else False
            })

            byBathroom = bool(node.get('extension') == "Lavatory")
            seat.update({
                "isbathroom": True if byBathroom else False
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

# print(seatInfo)
json_data = json.dumps(seatInfo)
print(json_data)

with open("info.json", "w") as json_file:
    json_file.write(json_data)
    json_file.close()