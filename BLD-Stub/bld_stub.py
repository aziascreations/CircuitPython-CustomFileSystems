# Constants

# Minimum sector size than can be requested to be read or written in the "readblocks" and "writeblocks" methods.
# Any call to these methods may use a multiple of this value.
MIN_SECTOR_SIZE = 512

# Code
class StubBlockDevice():
    # Incomplete stub for a generic block-device interface class.
    # See: https://docs.circuitpython.org/en/latest/shared-bindings/sdcardio/index.html
    
    def __init__(self):
        pass
    
    
    def count(self) -> int:
        # Returns the total number of sectors on the block-device as a multiple of "MIN_SECTOR_SIZE".
        return MIN_SECTOR_SIZE
    
    
    def deinit(self) -> None:
        # Disable permanently.
        pass
    
    
    def readblocks(self, start_block: int, buf: bytearray) -> None:
        # Read one or more blocks from the device.
        # The size of "buf" is a multiple of "MIN_SECTOR_SIZE".
        
        # Note:
        #   * The returned data is contained in the given buffer "buf".
        
        # Warning:
        #   * The official documentation says the "buf" parameter is typed as "circuitpython_typing.WriteableBuffer"
        #       although it is a "bytearray" in practice.
        pass
    
    
    def writeblocks(self, start_block: int, buf) -> None:
        # Writes one or more blocks from the device.
        # The size of "buf" is a multiple of "MIN_SECTOR_SIZE".
        
        # Warning:
        #   * The official documentation says the "buf" parameter is typed as "circuitpython_typing.WriteableBuffer"
        #       although it is a "???" in practice.  (Untested yet)
        pass
    
    
    def sync(self) -> None:
        # Ensure all blocks written are actually committed to the device.
        pass
