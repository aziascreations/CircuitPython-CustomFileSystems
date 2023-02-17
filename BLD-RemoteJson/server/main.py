# Imports
import io
import os

from flask import Flask, send_file

# Constants
HOST = "0.0.0.0"
PORT = 8080

BLD_FILE = "./bld.bin"
BLD_MIN_SECTOR_SIZE = 512
BLD_SECTOR_COUNT = 512  # 512 * 512 B = 256 KiB

HEX_DUMP_WIDTH = 32

# Globals
block_level_data: bytearray

# Code
print("Checking if '{}' exists...".format(BLD_FILE))
if not os.path.exists(BLD_FILE):
    print("> Couldn't find it, creating a new one...")
    
    with open(BLD_FILE, "wb") as f:
        f.write(b'\x00' * BLD_SECTOR_COUNT * BLD_MIN_SECTOR_SIZE)
    
    print("> Created a new file with {} sectors of {} bytes amounting to {} bytes.".format(
        BLD_SECTOR_COUNT, BLD_MIN_SECTOR_SIZE, BLD_SECTOR_COUNT * BLD_MIN_SECTOR_SIZE))

print("Loading the BLD file into memory...")
with open(BLD_FILE, "rb") as f:
    block_level_data = bytearray(f.read())

print("Preparing the Flask app...")
app = Flask(__name__)


@app.route('/')
def route_root():
    return """
    <!DOCTYPE html>
    <html lang="en-US">
    <head>
    <meta charset="utf-8">
    <title>BLD-RemoteJson Server Control Panel</title>
    </head>
    <body>
    <h1>BLD-RemoteJson Server Control Panel</h1>
    <h2>Actions</h2>
    <ul>
    <li><a href="/save">Save BLD to file.</a></li>
    <li><a href="/download">Download BLD to local machine.</a></li>
    <li><a href="/hexdump">Show HexDump of BLD.  <b>(May crash you tab if BLD is > 512 KiB !)</b></a></li>
    </ul>
    </body>
    </html>
    """


@app.route('/hexdump/')
def route_hexdump():
    print("Sending BLD hexdump to user...")
    return """
    <!DOCTYPE html>
    <html lang="en-US">
    <head>
    <meta charset="utf-8">
    <title>BLD-RemoteJson Server HexDump</title>
    <style>table{font-family: "Consolas";}</style>
    </head>
    <body>
    <h1>BLD-RemoteJson Server Control Panel</h1>
    <h2>Hex Dump</h2>
    <ul><li><a href="/">Return to main panel.</a></li></ul>
    <table>
    <thead><tr>
    <td>Offset</td>
    """ + "".join(["<td>" + hex(i) + "</td>" for i in range(HEX_DUMP_WIDTH)]) + """
    <td>Ascii</td>
    </tr></thead>
    <tbody>
    """ + "".join([
        "<tr><td>"+hex(i)+"</td>" + ("".join([
            "<td>" + hex(byte)[2:].upper() + "</td>"
            for byte in block_level_data[i:i + HEX_DUMP_WIDTH]
        ])) + "<td>" + ("." * HEX_DUMP_WIDTH) + "</td></tr>"
        for i in range(0, len(block_level_data), HEX_DUMP_WIDTH)
    ]) + """
    </tbody>
    </table>
    <ul><li><a href="/">Return to main panel.</a></li></ul>
    </body>
    </html>
    """


@app.route('/download/')
def route_download():
    print("Sending BLD copy to user...")
    return send_file(path_or_file=io.BytesIO(block_level_data), as_attachment=True, download_name="bld.bin")


@app.route('/save/')
def route_save():
    print("Saving BLD...")
    with open(BLD_FILE, "wb") as _f:
        _f.write(block_level_data)
    print("> Done !")
    
    return """
    <!DOCTYPE html>
    <html lang="en-US">
    <head>
    <meta charset="utf-8">
    <title>BLD-RemoteJson Server Control Panel</title>
    </head>
    <body>
    <h1>BLD-RemoteJson Server Control Panel</h1>
    <h2>Report</h2>
    <p>The file was properly saved on the server's side.</p>
    <ul><li><a href="/">Return to main panel.</a></li></ul>
    </body>
    </html>
    """


if __name__ == '__main__':
    print("Running server and its control panel on http://{}:{}".format(HOST, PORT))
    app.run(HOST, PORT)
