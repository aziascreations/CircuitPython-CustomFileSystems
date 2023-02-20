# Imports
import binascii
import gc
import json

import adafruit_requests


# Constants
BLD_MIN_SECTOR_SIZE = 512


# Code
class RemoteBlockDevice:
    # BLD class that accesses sectors from a given remote host.
    
    session: adafruit_requests.Session
    
    server_base_address: str
    server_timeout: int
    
    sector_count: int
    sector_size: int
    
    def __init__(self, session, server_base_address: str, server_timeout: int, sector_count: int, sector_size: int):
        self.session = session
        self.server_base_address = server_base_address
        self.server_timeout = server_timeout
        self.sector_count = sector_count
        self.sector_size = sector_size
    
    def count(self) -> int:
        """
        Returns the total number of sectors on the block-device.
        :return: Number of sectors on the block-device
        """
        return self.sector_count
    
    def readblocks(self, start_block: int, buf: bytearray) -> None:
        sector_count = int(len(buf) / BLD_MIN_SECTOR_SIZE)
        
        res = self.session.get("{}/data/?ssi={}&sc={}".format(
            self.server_base_address,
            start_block,
            sector_count
        ), timeout=self.server_timeout)
        
        if res.status_code != 200:
            raise OSError("Unable to grab {} sector(s) starting from sector #{}".format(sector_count, start_block))
        
        # Decoding the Base64-encoded sector data.
        data = binascii.a2b_base64(res.content)
        res.close()
        
        # Some final safety check
        if len(data) != len(buf):
            res.close()
            raise OSError("Requested {} byte(s) of data, got {} !".format(len(buf), len(data)))
        
        # Copying the data into the return buffer.
        for i in range(0, len(buf)):
            buf[i] = data[i]
        
        # Helping out the garbage collector  (Not really required)
        del res
        del data
        gc.collect()
    
    def writeblocks(self, start_block: int, buf: bytearray) -> None:
        sector_count = int(len(buf) / BLD_MIN_SECTOR_SIZE)
        data = binascii.b2a_base64(buf)
        
        res = self.session.post("{}/data/?ssi={}&sc={}".format(
            self.server_base_address,
            start_block,
            sector_count
        ), data=data, timeout=self.server_timeout)
        
        if res.status_code != 200:
            res.close()
            raise OSError("Unable to write {} sector(s) starting from sector #{}".format(sector_count, start_block))
        res.close()
        
        # Helping out the garbage collector  (Not really required)
        del res
        del data
        gc.collect()
    
    def deinit(self) -> None:
        """
        Disable the BLD permanently.
        :return: None
        """
        pass
    
    def sync(self) -> None:
        """
        Ensure all blocks written are actually committed to the device.
        :return: None
        """
        pass
