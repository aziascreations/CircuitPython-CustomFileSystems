# Imports
import io

# Constants
__FILE_SYSTEM_CONTENT = [
    ["test.txt",    "Hello world from a text file !"],
    ["test.py",     "print(\"> Hello world from a fake .py file :)\")"],
    ["__init__.py", ""],
]

# Code
class ReadOnlyMemoryFileSystem:
    label: str
    readonly: bool
    
    
    def __init__(self, label: str = "ROM", readonly: bool = False):
        # Preliminary check
        if len(label.encode('utf-8')) > 11:
            raise OSError("The given label '{}' is longer than 11 bytes !".format(label))
        
        self.label = label
        self.readonly = readonly
    
    
    def open(self, path: str, mode: str) -> Union[None, io.StringIO, io.BytesIO]:
        # Preliminary checks
        if not (mode in ["r", "rb", "rt"]):
            raise OSError("The mode '{}' isn't supported".format(mode))
            
        # Checking if the requested file exists
        requested_content: Union[None, str] = None
        
        for file_data in __FILE_SYSTEM_CONTENT:
            # Checking the filename  (The lstrip call is required !)
            if file_data[0] == path.lstrip("/"):
                requested_content = file_data[1]
                break
        
        if requested_content is None:
            # The file wasn't found.
            raise OSError("[Errno 2] No such file/directory: {}".format(path))
        
        # Returning the file's content.
        if mode.endswith("b"):
            return io.BytesIO(requested_content)
        else:
            return io.StringIO(requested_content)
    
    
    def stat(self, path: str) -> Tuple[int, int, int, int, int, int, int, int, int, int]:
        # If the file system's root folder is request, we just say it exists.
        if path == "/":
            return (0x4000, 0, 0, 0, 0, 0, 0, 0, 0, 0)
        
        # If we have any other path, we check if it is corresponds to one of the files provided by this file system.
        requested_content: Union[None, str] = None
        
        for file_data in __FILE_SYSTEM_CONTENT:
            # Checking the filename  (The lstrip call is required !)
            if file_data[0] == path.lstrip("/"):
                requested_content = file_data[1]
                break
        
        if not (requested_content is None):
            # We found the file.
            return (0x8000, 0, 0, 0, 0, 0, len(requested_content.encode("utf-8")), 0, 0, 0)
        
        # Saying we don't have the requested file or folder.
        raise OSError("[Errno 2] No such file/directory")
    
    
    def ilistdir(self, path: str) -> Iterator[Union[Tuple[AnyStr, int, int, int], Tuple[AnyStr, int, int]]]:
        # Returning the basic info of all the files in the root folder if requested.
        if path == "/":
            return iter([
                (file_data[0], 0x8000, 0, len(file_data[1].encode("utf-8"))) for file_data in __FILE_SYSTEM_CONTENT
            ])
        
        # An invalid path was given
        raise OSError("[Errno 2] No such file/directory")
    
    
    def statvfs(self, path: int) -> Tuple[int, int, int, int, int, int, int, int, int, int]:
        # We return a tuple saying the following:
        #   * Saying the we have a FS with 512 bytes blocks(0) and fragments(1)
        #   * We have a total of 1024 blocks(3) => 1024 * 512 B => 512 KiB
        #   * We have 896 blocks available in total(4), and 896 for unprivileged users(5) => 448 KiB
        #   * We have 0 inodes in total(6), 0 inodes free(7), and 0 inodes for unprivileged users(8)
        #   * We don't have mount flags (9) => 0 (Not used in CircuitPython, see CPython's official documentation)
        #   * The maximum filename is 255(10)
        return (512, 512, 1024, 896, 896, 0, 0, 0, 0, 255)
    
    
    def mkfs(self) -> None:
        return None
    
    
    def mkdir(self, path: str) -> None:
        return None
    
    
    def rmdir(self, path: str) -> None:
        return None
    
    
    def mount(self, readonly: bool, mkfs: VfsFat) -> None:
        return None
    
    
    def umount(self) -> None:
        return None
    
    
    def remove(self) -> None:
        # Warning:
        #   * The parameters to this method are unknown.
        #   * This method isn't documented at the time of writing.
        return None
    
    
    def chdir(self) -> None:
        # Warning:
        #   * The parameters to this method are unknown.
        #   * This method isn't documented at the time of writing.
        return None
    
    
    def getcwd(self) -> None:
        # Warning:
        #   * The parameters to this method are unknown.
        #   * This method isn't documented at the time of writing.
        return None
    
    
    def rename(self) -> None:
        # Warning:
        #   * The parameters to this method are unknown.
        #   * This method isn't documented at the time of writing.
        return None
    
    
    def utime(self) -> None:
        # Warning:
        #   * The parameters to this method are unknown.
        #   * This method isn't documented at the time of writing.
        return None
