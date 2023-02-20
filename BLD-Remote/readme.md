# CircuitPython - Custom File Systems - BLD-RemoteJson
This block-level device uses a remote server to store its sectors.

## Technical details
TODO

## Requirements

### Client
You need to install the [Adafruit Requests Library](https://github.com/adafruit/Adafruit_CircuitPython_Requests) into
your `/lib` folder.

The example code should notify you of any other potentially missing modules.

### Server
You need to install the `Flask` module in order for the server to work.

You can use one of the commands below:
```bash
pip install --upgrade Flask
pip install -r requirements.txt
```

## Running server
Simply run the [main.py](server/main.py) script and take note of the IP and port that will be given to you.

A simple administrative panel wan be accessed at the server's URL.<br>
This panel allows you to save and download the BLD to your computer in order to analyse it with other tools.

## Running client
Firstly, copy over the required libraries and the example code from the [client](client) folder.

Secondly, change the values in [secrets.py](client/secrets.py) to match your setup.

Finally, run the code and see the logs of both your server and client in order to see which sectors get read and written to for each operation.

## Going further
The BLD can be mounted on Windows if you use the [ImDisk's Ram Disk tool](https://sourceforge.net/projects/imdisk-toolkit/).

Once the volume is mounted, you can interact with the files in the save way you MCU can.
