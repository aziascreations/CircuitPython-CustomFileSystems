# Imports
import base64
import io
import json
import os
import time

from flask import Flask, send_file, request, Response

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


@app.route('/', methods=['GET'])
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
    <li><a href="/info">Show BLD info in JSON format.</a></li>
    </ul>
    </body>
    </html>
    """


@app.route('/data/', methods=['GET', 'POST'])
def search():
    # Grabbing and validating URL parameters.
    start_sector_index = int(request.args.get("ssi"))
    sector_count = int(request.args.get("sc"))
    
    if start_sector_index >= BLD_SECTOR_COUNT:
        print("The user requested the sector #{} but this BLD on has {} !".format(start_sector_index, BLD_SECTOR_COUNT))
        return Response("First requested sector is out-of-bounds", status=400)
    
    if start_sector_index + sector_count > BLD_SECTOR_COUNT:
        print("The user requested sectors that go out of the {} limit !".format(BLD_SECTOR_COUNT))
        return Response("Out-of-bounds sector(s) requested", status=400)
    
    # Checking which action needs to be taken.
    if request.method == 'POST':
        print("User sent {} sector(s) starting from {}".format(sector_count, start_sector_index))
        
        start_index = start_sector_index * BLD_MIN_SECTOR_SIZE
        end_index = start_index + (sector_count * BLD_MIN_SECTOR_SIZE)
        print("> Range: [{};{}[".format(start_index, end_index))
        
        # Decoding the data
        data = base64.b64decode(request.data)
        
        # Copying the data into memory
        for i in range(0, len(data)):
            block_level_data[start_index + i] = data[i]
        
        return Response("", status=200)
    else:
        print("User requested {} sector(s) starting from {}".format(sector_count, start_sector_index))
        
        start_index = start_sector_index * BLD_MIN_SECTOR_SIZE
        end_index = start_index + (sector_count * BLD_MIN_SECTOR_SIZE)
        print("> Range: [{};{}[".format(start_index, end_index))
        
        return Response(base64.b64encode(block_level_data[start_index: end_index]), status=200)


@app.route('/info/', methods=['GET'])
def route_info():
    print("Sending BLD info...")
    return json.dumps({
        "sector_size": BLD_MIN_SECTOR_SIZE,
        "sector_count": BLD_SECTOR_COUNT,
        "server_time": int(time.time())
    })


@app.route('/download/', methods=['GET'])
def route_download():
    print("Sending BLD copy to user...")
    return send_file(path_or_file=io.BytesIO(block_level_data), as_attachment=True, download_name="bld.bin")


@app.route('/save/', methods=['GET'])
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
