#!/usr/bin/env python
"""Convert ECOMCat CAN message trace files to the OpenXC raw message format.

    $ ./ecomcat_to_openxc example.dat > example-openxc.json
"""

import fileinput
import json

ID_HIGH_NAME = "IDH"
ID_LOW_NAME = "IDL"
DATA_NAME = "Data"
LENGTH_NAME = "Len"
REQUIRED_INPUT_ATTRS = (ID_HIGH_NAME, ID_LOW_NAME, DATA_NAME, LENGTH_NAME,)

def convert_ecomcat_to_openxc():
    for line in fileinput.input():
        tokens = line.split(",")
        data = {}
        for token in tokens:
            name, value = token.split(":")
            data[name.strip()] = value.strip()

        contains_required_attributes = True
        for attribute in REQUIRED_INPUT_ATTRS:
            if attribute not in data:
                contains_required_attributes = False
                break

        data[DATA_NAME] = "0x%s" % "".join(data[DATA_NAME].split(" ")).lower()

        if contains_required_attributes:
            openxc_formatted_data = {
                'id': int("0x%s%s" % (
                        data[ID_HIGH_NAME], data[ID_LOW_NAME]), 0),
                'length': int(data[LENGTH_NAME]),
                'data': data[DATA_NAME]
            }
            print(json.dumps(openxc_formatted_data))

if __name__ == "__main__":
    convert_ecomcat_to_openxc()
