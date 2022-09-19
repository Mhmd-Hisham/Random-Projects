#!/usr/bin/env python3
#
# TODO:-
# shred links
#

import os
import sys
import shutil
import random
import string
import argparse

CHARS = string.punctuation + string.ascii_letters + string.digits

def opt_parser():
    parser = argparse.ArgumentParser(
        description="""Overwrite the specified FILE(s) repeatedly, in order to make it harder
for even very expensive hardware probing to recover the data. It can also shred directories.""")

    parser.add_argument(
        "paths", 
        help="directory/file name to shred, you can specify more than one directory/file.", 
        nargs='+', 
        metavar="dir(s)"
    )
    parser.add_argument(
        "-u", 
        "--remove", 
        help="truncate and remove file/directory after overwriting.",
        dest="remove", 
        action="store_true",
        default=False
    )
    parser.add_argument(
        "-R", 
        "--recursive", 
        help="Shred subdirectories recursively.",
        dest="recursive", 
        action="store_true",
        default=False
    )
    parser.add_argument(
        "-n", 
        "--iterations", 
        help="overwrite N times instead of the default (3)",
        dest="passes", 
        type=int, 
        default=3
    )

    parser.add_argument(
        "-z", 
        "--zero", 
        help="add a final overwrite with zeros to hide shredding",
        dest="zero", 
        action="store_true",
        default=False
    )

    return parser.parse_args()


def shred_file_data(pathname, passes, zero):
    # basename = os.path.basename(pathname)
    # dirname = os.path.dirname(pathname)

    length = os.path.getsize(pathname)

    with open(pathname, "wb") as fh:
        for _ in range(passes):
            char = CHARS[random.randrange(0, 94)]
            fh.seek(0, 0)
            fh.write(bytes(char*length, encoding='utf-8'))
            fh.flush()

        if (zero):
            fh.seek(0, 0)
            fh.write(bytes('\00'*length, encoding='utf-8'))
            fh.flush()

    return 0


def shred_filename(pathname):
    basename = os.path.basename(pathname)
    for i in range(len(basename), 0, -1):
        dirname = os.path.dirname(pathname)
        new_name = os.path.join(dirname, '0'*i)
        try:
            os.renames(pathname, new_name)
            pathname = new_name
        except OSError as e:
            print(e)
            # there is no need to continue if we can't rename at a level..
            break
    return new_name


def main():
    options = opt_parser()
    directories, files = [], []

    for path in options.paths:
        if os.path.isdir(path):
            directories.append(path)

        elif os.path.isfile(path):
            files.append(path)

    if options.recursive:
        for directory in directories:
            for root, dirs, _files in os.walk(directory):
                for _dir in dirs:
                    dirname = os.path.join(root, _dir)
                    if (dirname not in directories):
                        directories.append(dirname)

                for _file in _files:
                    filename = os.path.join(root, _file)
                    if (filename not in files):
                        files.append(filename)

    # sort by depth..
    directories.sort(key=lambda a: len(a.split(os.path.sep)), reverse=True)

    for pathname in files:
        if os.path.isfile(pathname) and os.path.exists(pathname):
            shred_file_data(pathname, passes=options.passes, zero=options.zero)

            if options.remove:
                pathname = shred_filename(pathname)
                os.remove(pathname)

    for pathname in directories:
        if os.path.exists(pathname) and os.path.isdir(pathname):
            if options.remove:
                pathname = shred_filename(pathname)
                os.rmdir(pathname)

    return 0


if __name__ == "__main__":
    main()
    sys.exit()
