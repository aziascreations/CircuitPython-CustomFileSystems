# Imports
import io

# Code
class BlankMemoryFileSystem:
    # The filesystem label, up to 11 case-insensitive bytes.
    label: str
    
    # Whether the sile system should be in read-only mode or not.
    readonly: bool
    
    def __init__(self, label: str = "BLANK", readonly: bool = False):
        # Note: We don't pass a block-device object in the constructor since we won't be interacting with one in this
        #        file system.
        
        # Preliminary check
        if len(label.encode('utf-8')) > 11:
            raise OSError("The given label '{}' is longer than 11 bytes !".format(label))
        
        self.label = label
        self.readonly = readonly
    
    def mkfs(self) -> None:
        # Called when the filesystem needs to be reformatted and have all its data deleted.
        return None
    
    def open(self, path: str, mode: str) -> Union[None, io.StringIO, io.BytesIO]:
        # Called when a file need to be 
        # Should act like the builtin `open()`.
        
        # Notes:
        #   * The returned types should be changed from their original types, as indicated in CircuitPython's
        #       documentation to their instantiable equivalents shown below:
        #     * io.TextIOWrapper => io.StringIO
        #     * io.FileIO        => io.BytesIO
        #   * Failure to do so will very likely result in your MCU experiencing a hard-reset caused by a internal error !
        #   * The potential modes received should be the following:
        #     * r, rb, rt
        #     * w, wb, wt
        #   * The `r` and `w` modes appear to be considered as their `rt` and `wt` equivalents in CircuitPython.
        #   * Any invalid type should raise the following: `ValueError("Invalid mode")`
        #   * Any delay in the execution of this method doesn't see to upset CircuitPython itself.
        #     * Doesn't throw error even if it takes more than one minute to return.
        
        # Warning:
        #   * CircuitPython appears to raise the error in the code below when attempting to open directories.
        #   * Exemple:
        #      import storage
        #      root = storage.getmount("/")
        #      f = root.open("/lib", "r")  # Doesn't work, even if the standard folder is present !
        #      f = root.open("lib", "r")   # Same as above.
        
        # We cannot find the requested file/folder.
        raise OSError("[Errno 2] No such file/directory: {}".format(path))
    
    def stat(self, path: str) -> Tuple[int, int, int, int, int, int, int, int, int, int]:
        # Similar to `os.mkdir`.
        # Returns a tuple that contains various informations and properties about a requested file or folder.
        
        # Returned data:  (in order) (See: https://docs.python.org/3/library/os.html#os.stat_result)
        #   * Flags (0x4000 = Folder, 0x8000 = File)
        #   * File's inode number/file index  (Should be left as `0`)
        #   * Parent device's identifier      (Should be left as `0`)
        #   * Number of hard links.  (Should be left as `0`)
        #   * Owner's user ID        (Should be left as `0`)
        #   * Owner's group ID       (Should be left as `0`)
        #   * File's size in bytes   (Should be `0` for folders)
        #   * Timestamp of the most recent access        (In seconds as unix timestamp, can be 0)
        #   * Timestamp of the most recent modification  (In seconds as unix timestamp, can be 0)
        #   * Timestamp of the most recent metadata change on Unix, or creation on Windows  (In seconds as unix timestamp, can be 0)
        
        # Warning:
        #   * This method appears to be silently called when the file-system is mounted as it can fail if you return
        #       `None` but works perfectly when you return a proper tuple for "/".
        #   * The "silently called" part comes from the fact that `print()` calls during a proper and successfull mount
        #       don't appear in the REPL shell.
        
        # If the file system's root folder is request, we just say it exists
        if path == "/":
            return (0x4000, 0, 0, 0, 0, 0, 0, 0, 0, 0)
        
        # Saying we don't have the requested file or folder.
        # This is REQUIRED for CircuitPython as it uses this exception to determine whether a file/folder exists when processing imports.
        raise OSError("[Errno 2] No such file/directory")
    
    def statvfs(self, path: int) -> Tuple[int, int, int, int, int, int, int, int, int, int]:
        # Similar to `os.mkdir`.
        # Returns a tuple that contains various informations and properties about file system in which the given path is located.
        
        # Notes:
        #   * If called by `os.statvfs`, the mounting point will be ommited and will be relative to this file system's root folder.
        #   * The value is returned by this method is returned as-is by `os.statvfs`.
        
        # Warning:
        #   * The returned tuple doesn't contain the `f_fsid` value as CPython's `os.statvfs` does.
        
        # Links:
        #   * https://docs.circuitpython.org/en/latest/shared-bindings/os/index.html#os.statvfs
        #   * https://docs.python.org/3/library/os.html#os.statvfs
        #   * https://www.geeksforgeeks.org/python-os-statvfs-method/
        
        # We return a tuple saying the following:
        #   * Saying the we have a FS with 512 bytes blocks(0) and fragments(1)
        #   * We have a total of 1024 blocks(3) => 1024 * 512 B => 512 KiB
        #   * We have 896 blocks available in total(4), and 896 for unprivileged users(5) => 448 KiB
        #   * We have 0 inodes in total(6), 0 inodes free(7), and 0 inodes for unprivileged users(8)
        #   * We don't have mount flags (9) => 0 (Not used in CircuitPython, see CPython's official documentation)
        #   * The maximum filename is 255(10)
        return (512, 512, 1024, 896, 896, 0, 0, 0, 0, 255)
    
    def ilistdir(self, path: str) -> Iterator[Union[Tuple[AnyStr, int, int, int], Tuple[AnyStr, int, int]]]:
        # Return an iterator whose values describe files and folders within the given `path`.
        # The given path is relative to this file system's root and not its mounting point.
        
        # Returned data:  (in order)
        #   * Filename
        #   * Flags    (0x4000 = Folder, 0x8000 = File)
        #   * Unknown  (Leave as 0)
        #   * File's size in bytes   (Should be `0` for folders)
        
        # Here is an example of a root directory with only one file:
        # ```python
        # iter([
        #     ("test.txt", 32768, 0, ???),  # Change the "???" by the actual file's size.
        # ])
        # ```
        
        # Returning an empty root directory.
        return iter([])
    
    def mkdir(self, path: str) -> None:
        # Same as `os.mkdir`
        return None
    
    def rmdir(self, path: str) -> None:
        # Same as `os.rmdir`
        return None
    
    def mount(self, readonly: bool, mkfs: VfsFat) -> None:
        # Called when mounting with `storage.mount`.
        # Don’t call this directly.
        
        # Notes:
        #   * The given "mkfs" value is equal to self.
        
        return None
    
    def umount(self) -> None:
        # Called when unmounting with `storage.umount`.
        # Don’t call this directly.
        return None
    
    # Some methods are apparently missing from CircuitPython's documentation at the time of writing.
    # I'll make stubs here in order to force an explicit error if CircuitPython calls them complaining about the number of parameters.
    # I prefer to have them just in case it throw a silent internal error if it can't find them.
    
    def remove(self) -> None:
        # Called when deleting a file.
        
        # Warning:
        #   * The parameters to this method are unknown.
        #   * This method isn't documented at the time of writing.
        
        return None
    
    def chdir(self) -> None:
        # ???
        
        # Warning:
        #   * The parameters to this method are unknown.
        #   * This method isn't documented at the time of writing.
        
        return None
    
    def getcwd(self) -> None:
        # ???
        
        # Warning:
        #   * The parameters to this method are unknown.
        #   * This method isn't documented at the time of writing.
        
        return None
    
    def rename(self) -> None:
        # Called when renaming a file.
        
        # Warning:
        #   * The parameters to this method are unknown.
        #   * This method isn't documented at the time of writing.
        
        return None
    
    def utime(self) -> None:
        # ???
        
        # Warning:
        #   * The parameters to this method are unknown.
        #   * This method isn't documented at the time of writing.
        
        return None
