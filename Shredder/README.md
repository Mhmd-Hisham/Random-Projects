

## Description

A cross-platform python script that mimics the "shred" command in Linux. Uses built-in libraries only. 

You can shred files and directories recursively with multiple passes.

It also has a simple command-line interface.


## Usage

```
usage: shredder.py [-h] [-u] [-R] [-n PASSES] [-z] dirs) [dir(s ...]

Overwrite the specified FILE(s) repeatedly, in order to make it harder for even very expensive hardware probing to recover
the data. It can also shred directories.

positional arguments:
  dir(s)                directory/file name to shred, you can specify more than one directory/file.

optional arguments:
  -h, --help            show this help message and exit
  -u, --remove          truncate and remove file/directory after overwriting.
  -R, --recursive       Shred subdirectories recursively.
  -n PASSES, --iterations PASSES
                        overwrite N times instead of the default (3)
  -z, --zero            add a final overwrite with zeros to hide shredding
```

## Meta

Mohamed Hisham – [Gmail](mailto:Mohamed00Hisham@Gmail.com) | [GitHub](https://github.com/Mhmd-Hisham) | [LinkedIn](https://www.linkedin.com/in/Mhmd-Hisham/)

## License
This project is licensed under the GNU GPLv3 License - check [LICENSE](../LICENSE) for more details.