import os
import glob
import sys
import fnmatch


def remove_temp_files():
    """Removes all temp files"""
    path = os.getcwd()
    files = glob.glob(path + '/*', recursive=True)

    for file in files:
        if 'TEMP' in file:
            os.remove(file)

        if '_clicks' in file:
            os.remove(file)


    