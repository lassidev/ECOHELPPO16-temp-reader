#!/usr/bin/env python3

from gattlib import GATTRequester
# couldnt get gattlib to return the device's name for whatever reason, so bleakscanner is used instead
from bleak import BleakScanner
import asyncio

async def scanner(wanted_name):
    device = await BleakScanner.find_device_by_filter(
        lambda d, ad: d.name and d.name.lower() == wanted_name.lower()
    )
    return device

print("Scanning for thermostats...")

# get the thermostat MAC address
device = asyncio.run(scanner("Tael"))

print("MAC address for the ECOHELPPO16 thermostat: {}".format(device.address))


req = GATTRequester(device.address, False)
# connect with channel type random, https://novelbits.io/bluetooth-address-privacy-ble/
req.connect(True, channel_type="random")
# GATT handle 0x001a has all the three temp values in hex
# Format will be something like \x00\x00\x00\x00\x04\x01\xf8\x00\xba\x00\x00\x00
temps = req.read_by_handle(0x1a)[0]

# get desired temp hex and reverse
desiredtempbytes = temps[4:6][::-1]
# convert to float and divide by 10 to get the correct decimal temp in celcius
desiredtemp = float.fromhex(desiredtempbytes.hex()) / 10
# get air temp hex and reverse
airtempbytes = temps[6:8][::-1]
# convert to float and divide by 10 to get the correct decimal temp in celcius
airtemp = float.fromhex(airtempbytes.hex()) / 10
# get floor temp hex and reverse
floortempbytes = temps[8:10][::-1]
# convert to float and divide by 10 to get the correct decimal temp in celcius
floortemp = float.fromhex(floortempbytes.hex()) / 10

print("DESIRED TEMP: {}°C".format(desiredtemp))
print("AIR TEMP: {}°C".format(airtemp))
print("FLOOR TEMP: {}°C".format(floortemp))
