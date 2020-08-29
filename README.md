# Airline Seat Data Parser
API which extracts airline seat information from an
online travel agency's (OTA) legacy booking system.

## Development Environment
### Language
- Python 3.8.1

### Libraries
- xml.etree.ElementTree
- json

## Installation
Clone this repo to your local machine:
```
git clone https://github.com/wmemorgan/xml-seat-data-parser.git
```

## Usage
Go to the **src** directory in your local repository and run the script
```
python main.py
```

## Output
Script creates a file in the **output** directory named `seatinfo.json`.

## Data Dictionary
The JSON file contains the following data fields:
| Field | Type | Description |
| --- | --- | --- |
| **class** | string | Cabin class
| **isavailable** | boolean | Seat availability for purchase
| **isbathroom** | boolean | Seat is next to the bathrom
| **ispreferred** | boolean | Seat flagged as Preferred status
| **location** | string | Seat location
| **planesection** | string | Location of seat on the plane
| **price** | integer | Ticket price (USD) of available seat. **NOTE**: Reports a '0' price if seat is unavailable.
| **rowtype** | string | Location of row on the plane (i.e. exit row, bulkhead, standard row)
| **seatnumber** | string | Seat number


## License
[MIT](https://github.com/wmemorgan/xml-seat-data-parser/blob/master/LICENSE)