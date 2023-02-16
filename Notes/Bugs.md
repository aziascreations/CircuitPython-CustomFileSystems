# Bugs & problems observed

## Invalid mounting point
When mounting a file system, it appears CircuitPython doesn't correctly processes the given mounting point's path and
only trims the first character.

Here are a couple of examples to illustrate this issue:
| Given mount point | Folder's name in `os.listdir()` |
|-------------------|---------------------------------|
|`/test`            |`"test"`                         |
|`/test/`           |`"test/"`                        |
|`test`             |`"est"`                          |

Additionally, is you want to mount a directory inside another directory, it doesn't appear to be properly listed when
listing a folder's content with the `os.listdir()` method.

For example, if we were to mount a file system onto `/lib/myfs`, we cannot see it when listing the content of the
standard `/lib` folder.<br>
However, if we list the content of the root folder, we can see it as `lib/myfs` alongside the `lib` folder.

## Missing methods in documentation
Some methods implemented in the [VfsFat](https://docs.circuitpython.org/en/latest/shared-bindings/storage/index.html#storage.VfsFat) class aren't properly explained in the documentation.

Their signature is unknown and can only be seen when using `dir()` on the root filesystem.

They are likely used when calling their equivalent from the `os` module, however, this wasn't tested just yet.

| Fields & methods | In [documentation](https://docs.circuitpython.org/en/latest/shared-bindings/storage/index.html#storage.VfsFat) | In `storage.VFSFat` | Used during normal operation |
|------------------|------------------|---------------------|------------------------------|
| label            | ✔               | ✔                  | ❔                            |
| readonly         | ✔               | ✔                  | ❔                            |
| mkfs             | ✔               | ✔                  | ✔                            |
| open             | ✔               | ✔                  | ✔                            |
| ilistdir         | ✔               | ✔                  | ✔                            |
| mkdir            | ✔               | ✔                  | ❔                            |
| rmdir            | ✔               | ✔                  | ❔                            |
| stat             | ✔               | ✔                  | ✔                            |
| statvfs          | ✔               | ✔                  | ✔                            |
| mount            | ✔               | ✔                  | ✔                            |
| umount           | ✔               | ✔                  | ❔                            |
| remove           | ❌               | ✔                  | ❔                            |
| chdir            | ❌               | ✔                  | ❔                            |
| getcwd           | ❌               | ✔                  | ❔                            |
| rename           | ❌               | ✔                  | ❔                            |
| utime            | ❌               | ✔                  | ❔                            |
