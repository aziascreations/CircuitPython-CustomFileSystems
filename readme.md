# CircuitPython - Custom File Systems
This repo contains multiple experiments with virtual file system for [CircuitPython](https://github.com/adafruit/circuitpython)
that attempt to emulate a conventional storage device at the file system and block-device level.

One of 

The second main advantage is as an educational tool due to the [permissive] nature of Python and CircuitPython's APIs
which allows you to easily test different low-level [???] and effectively log their behaviour.

## Warning
This project is an experiment and shouldn't be used in any production or remotely sensitive environment as
they are vulnerable to many types of attacks if you don't modify them in order to secure them further.

In CircuitPython 8.0, it apperas to be impossible to mount [...].

## Requirements
* A device with CircuitPython 8.0 or newer flashed onto it.
  * Access to the [zlib](https://docs.circuitpython.org/en/latest/shared-bindings/zlib/index.html) module is required for most block-level projects due to space constraints.
  * Wi-Fi connectivity is required for some projects.
  * It is recommended to have around 1 MiB of disk space and 48 KiB of RAM free on the device itself.
* A way to mount disk images on you computer for block-level projects.
  * [ImDisk's Ram Disk tool](https://sourceforge.net/projects/imdisk-toolkit/) is recommended for Windows.
  * I don't know about Linux, sorry.
* A lot of patience to deal with some of CircuitPython's quirks.
  * See the [???](#) document for more info on some of the bug found during this project.

## Summary
* File Systems
  * Blank
* Block-level devices
  * <s>Blank</s> (TODO)

## File Systems

### [Blank](FS-Blank)
Blank file system with a lot of comments on how each procedure works and what it should return.<br>
When its content is listed, it is shown as being empty.

## License
This repo is license under the [MIT license](LICENSE).
