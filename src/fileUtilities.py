"""Manage Files

This module handles file importing and exporting.

The module imports the following functions:
    * xml.etree.ElementTree - parsing and creating XML data
    * json - JSON encoder and decoder

The module contains the following functions:
    * read_xml_file - reads xml data and extracts specified elements
    * create_json_file - converts data to JSON format
"""

import xml.etree.ElementTree as ET
import json

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

def create_json_file(data, output_filename):
    """Converts data to JSON format and exports file

    Parameters
    ----------
    data : list
        Data to be published
    output_filename : str
        Output filename

    Returns
    -------
    json
        a list of seat data

    """

    json_data = json.dumps(data)

    with open(f"../output/{output_filename}", "w") as json_file:
        json_file.write(json_data)
        json_file.close()
