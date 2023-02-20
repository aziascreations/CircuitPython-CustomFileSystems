# MCU's entrypoint

# Checking if we are on CircuitPython.
import sys
if sys.implementation.name != "circuitpython":
    print("ERROR: You are not using a CircuitPython-based implementation of Python !")
    sys.exit(1)


# Checking if we have access to the required optional modules.
try:
    import wifi
except ImportError:
    print("Unable to import the 'wifi' module !")
    print("You need to use a MCU and firmware that supports this module.")
    sys.exit(2)

try:
    import binascii
except ImportError:
    print("Unable to import the 'binascii' module !")
    print("You need to use a MCU and firmware that supports this module.")
    sys.exit(3)

try:
    import adafruit_requests
except ImportError:
    print("Unable to import the 'adafruit_requests' module !")
    print("You need to download and install it onto your device.")
    sys.exit(4)

try:
    import secrets
except ImportError:
    print("Unable to import the 'secrets' module !")
    print("You need to use the one provided in the repository and add your values.")
    sys.exit(5)


# Imports
import json
import os
import random
import socketpool
import storage
import wifi

import bld_remote
from secrets import secrets


# CONSTANTS
MOUNTING_POINT = "/remote_bld"

FORMAT_BEFORE_MOUNT = True

WIFI_SSID = secrets["ssid"]
WIFI_PASS = secrets["password"]

SERVER_TIMEOUT = 10
SERVER_BASE_ADDRESS = "http://{}:{}".format(secrets["server_host"], secrets["server_port"])


# Code
print("Preparing the Wi-Fi connection...")
wifi.radio.enabled = True

print("> Connecting to '{}'".format(WIFI_SSID))
try:
    wifi.radio.connect(WIFI_SSID, WIFI_PASS)
    print("> Done !")
    print("> IPv4: {}".format(wifi.radio.ipv4_address))
except:
    print("ERROR: Failed to establish a Wi-Fi connection !")
    sys.exit(6)


print("Preparing the socketpool and session for the BLD...")
pool = socketpool.SocketPool(wifi.radio)
session = adafruit_requests.Session(pool)


# This step is required in order to instantiate a BLD class that reports having the same amount of sectors as
#  the server has.
print("Grabbing the BLD info from the remote server...")
print("> GET: {}/info/".format(SERVER_BASE_ADDRESS))
try:
    res = session.get("{}/info/".format(SERVER_BASE_ADDRESS), timeout=SERVER_TIMEOUT)
except:
    print("> ERROR: Failed to get info !")
    print("> If this issue persists on a windows-hosted server, try checking your firewall settings.")
    sys.exit(7)

if res.status_code != 200:
    print("> ERROR: Got an unexpected status code !  ({})".format(res.status_code))
    res.close()
    sys.exit(8)

print("> Parsing JSON data...")
bld_info = json.loads(res.content)
res.close()
print("> {}".format(bld_info))


print("Preparing the BLD class...")
print("> Sector count: {}".format(bld_info["sector_count"]))
print("> Sector size:  {}".format(bld_info["sector_size"]))
bld = bld_remote.RemoteBlockDevice(
    session=session,
    server_base_address=SERVER_BASE_ADDRESS,
    server_timeout=SERVER_TIMEOUT,
    sector_count=bld_info["sector_count"],
    sector_size=bld_info["sector_size"],
)


print("Preparing the VfsFat...")
fs = storage.VfsFat(bld)

if FORMAT_BEFORE_MOUNT:
    print("> Doing a quick format of the file system using the builtin formatter.  (This may take a while !)")
    fs.mkfs(bld)
else:
    print("> Skipping the formatting step.  (It needs to have been done at least ONCE before !)")

print("> Mounting the file system at '{}' in RW mode...".format(MOUNTING_POINT))
storage.mount(fs, MOUNTING_POINT, readonly=False)


print("Checking if we can see it in the MCU's root folder:")
print("> {}".format(os.listdir("/")))
if MOUNTING_POINT.lstrip("/") in os.listdir("/"):
    print("> It is present !")
else:
    print("> It couldn't be found, exiting !")
    sys.exit(9)


print("Creating a new file under '{}'".format(MOUNTING_POINT + "/test.txt"))

unique_number = int(random.random() * 100)
print("> Unique number: {}".format(unique_number))

with open(MOUNTING_POINT + "/test.txt", "w") as f:
    f.write("Hello world !  ({})".format(unique_number))
print("> Done !")

print("> Reading it...")
with open(MOUNTING_POINT + "/test.txt", "r") as f:
    print("> {}".format(f.read()))


print("Creating a new python file under '{}'".format(MOUNTING_POINT + "/test.py"))

unique_number = int(random.random() * 100)
print("> Unique number: {}".format(unique_number))

with open(MOUNTING_POINT + "/test.py", "w") as f:
    f.write("print(\"> Hello world !  ({})\")".format(unique_number))
print("> Done !")


print("Preparing the 'sys.path' list to let us import from the new file system")
print("> Old: {}".format(sys.path))
sys.path.insert(0, MOUNTING_POINT)
print("> New: {}".format(sys.path))


print("Importing the 'test' module from '{}'".format(MOUNTING_POINT + "/test.py"))
import test
