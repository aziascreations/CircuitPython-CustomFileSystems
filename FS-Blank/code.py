# MCU's entrypoint

# Checking if we are on CircuitPython.
import sys
if sys.implementation.name != "circuitpython":
    print("ERROR: You are not using a CircuitPython-based implementation of Python !")
    sys.exit(1)

# Imports
import os
import storage

import fs_blank

# CONSTANTS
MOUNTING_POINT = "/mfs"

# Code
print("Preparing the blank file system...")
fs = fs_blank.BlankMemoryFileSystem()

print("Mounting the blank file system in '{}' ...".format(MOUNTING_POINT))
storage.mount(fs, MOUNTING_POINT)

print("Checking if we can see it in the MCU's root folder:")
if MOUNTING_POINT.lstrip("/") in os.listdir("/"):
    print("> It is present !")
else:
    print("> It couldn't be found, exiting !")
    sys.exit(2)

print("Listing of '{}'".format(MOUNTING_POINT))
for element in os.listdir(MOUNTING_POINT):
    print("> {}".format(MOUNTING_POINT))
