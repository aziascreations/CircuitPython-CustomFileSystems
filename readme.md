# CircuitPython - Custom File Systems
This repo contains multiple experiments with virtual file system for [CircuitPython](https://github.com/adafruit/circuitpython)
that attempt to emulate a conventional storage device at the file system and block-device level.

## Preamble
One of the main advantage of this project is that it give you a strong, clear, and documented starting point for future
experiments that may require virtual file systems and block-level devices.

For example, by using the blank examples, you can easily create a bootstrapping code and file system that connects
securely to a remote server and pulls code directly from it without ever having touch the disk.<br>
This is, at the very least, an interesting experiment from a data forensics and security point-of-view as it forces you
to dabble in and learn a bit in both of these fields.

The second main advantage is as an educational tool.<br>
Due to the permissive nature of Python and CircuitPython's APIs, it lets someone test out different designs and
mechanisms for their file systems without running the risk of corrupting unrelated data or bricking their device.
Additionally, it is possible add logging to many of the methods which in turn allows you to see and understand parts of
the inner workings of CircuitPython itself.

## Warning
This project is an experiment and shouldn't be used as-is in any production or remotely sensitive environment as
they are vulnerable to many types of attacks if you don't modify them in order to secure them further.

In CircuitPython 8.0, it appears to be impossible to properly mount a file system inside another folder than the
device's root folder.<br>
See "[Notes -> Bugs -> Invalid Mounting Point](Notes/Bugs.md#invalid-mounting-point)" for more info.

## Requirements
* A device with CircuitPython 8.0 or newer flashed onto it.
  * Access to the [zlib](https://docs.circuitpython.org/en/latest/shared-bindings/zlib/index.html) module is required for most block-level projects due to space constraints.
  * Wi-Fi connectivity is required for some projects.
  * It is recommended to have around 1 MiB of disk space and 48 KiB of RAM free on the device itself.
* A way to mount disk images on you computer for block-level projects.
  * [ImDisk's Ram Disk tool](https://sourceforge.net/projects/imdisk-toolkit/) is recommended for Windows.
  * I don't know about Linux, sorry.
* A lot of patience to deal with some of CircuitPython's quirks.
  * See the "[Notes -> Bugs](/Notes/Bugs.md)" document for more info on some bugs found during this project.

## Summary
* File Systems
  * Blank
  * Read-Only Memory
* Block-level devices
  * Stub

## File Systems

### [Blank](FS-Blank)
Blank file system with a lot of comments on how each procedure works and what it should return.<br>
When its content is listed, it is shown as being empty.

This file system has a LOT more comments than the others which explains in much more details how each important method works.

### [Read-Only Memory](FS-ReadOnlyMemory)
Simple read-only file system that provides 3 files contained within a private constant in the "[fs_rom.py](FS-ReadOnlyMemory/fs_rom.py)" file.

The goal of this file system is to illustrate how directory listings are done, and how files openned in `r*` modes are handled internally.

## Block-level Devices

### [Stub](BLD-Stub)
Stub of a generic block-level class without any code, but detailed comments for each required methods and their warnings and notes.

The reasoning behind not making this one a working class is that block-level devices require quite a bit more code to
make them work as you need to create a working MBR and FAT partition.

## License
This repo is license under the [MIT license](LICENSE).
