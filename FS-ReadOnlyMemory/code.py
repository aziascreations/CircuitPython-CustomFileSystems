# MCU's entrypoint

# Checking if we are on CircuitPython.
import sys
if sys.implementation.name != "circuitpython":
    print("ERROR: You are not using a CircuitPython-based implementation of Python !")
    sys.exit(1)

# Imports
import os
import storage

import fs_rom

# CONSTANTS
MOUNTING_POINT = "/rom"

# Code
print("Preparing the read-only memory file system...")
fs = fs_rom.ReadOnlyMemoryFileSystem()


print("Mounting the file system in '{}' ...".format(MOUNTING_POINT))
storage.mount(fs, MOUNTING_POINT)


print("Checking if we can see it in the MCU's root folder:")
print("> {}".format(os.listdir("/")))
if MOUNTING_POINT.lstrip("/") in os.listdir("/"):
    print("> It is present !")
else:
    print("> It couldn't be found, exiting !")
    sys.exit(2)


print("Listing of '{}':".format(MOUNTING_POINT))
for element in os.listdir(MOUNTING_POINT):
    print("> {}".format(element))


print("Checking if some required files exist")

if not ("test.txt" in os.listdir(MOUNTING_POINT)):
    print("> Cannot find 'test.txt' !")
    sys.exit(3)

if not ("test.py" in os.listdir(MOUNTING_POINT)):
    print("> Cannot find 'test.py' !")
    sys.exit(4)

print("> Everything seems fine :)")


print("Reading the '{}' file.".format(MOUNTING_POINT + "/test.txt"))
print("> Mode 'r'")
with open(MOUNTING_POINT + "/test.txt", "r") as f:
    print("> Content: {}".format(f.read()))
print("> Mode 'rb'")
with open(MOUNTING_POINT + "/test.txt", "rb") as f:
    print("> Content: {}".format(f.read()))


print("Preparing the 'sys.path' list to let us import from the new file system")
print("> Old: {}".format(sys.path))
sys.path.insert(0, MOUNTING_POINT)
print("> New: {}".format(sys.path))


print("Importing the 'test' module from '{}'".format(MOUNTING_POINT + "/test.py"))
import test
