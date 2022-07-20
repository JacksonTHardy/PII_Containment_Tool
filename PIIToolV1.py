#!/usr/bin/env python

# Import the os module
import os
from os import listdir
from os.path import isfile, isdir, join
from pathlib import Path
import re
import subprocess

flagged_files: list[str] = []


def getfiles(directory: str, filelist: list[str]) -> list[str]:
    # print("Current working directory: {0}".format(directory))

    for file in listdir(directory):  # for each file in the listdir
        path = join(directory, file)  # concats directory with the file
        if isdir(path):  # determines if path is a exsisting directory or not
            filelist = getfiles(path, filelist)
        elif isfile(path):  # determines if path exist as a file
            filelist.append(path)  # if file exist it adds it to a list of all files
        else:
            print("Error with current directory: {0}".format(path))

    return filelist  # returns a list of all the file names that exist


def processfiles(completefilelist: list):
    """_summary_
    Next: store files, prompt user to open flagged files.
    Args:
        completefilelist (list): _description_
    """
    for file in completefilelist:
        ext: str = Path(file).suffix  # saves the file suffix like .txt into ext
        match ext:
            # if the file ends in one of the following extensions
            case ".txt" | ".csv" | ".json" | ".xml":
                scanfile(file)


def scanfile(file: str):
    with open(file, "r") as f:
        has_ssn: bool = False
        file_contents: str = f.read()
        if re.search(
            "national[\\s_]?id|social[\\s_]?security[\\s_]?number|ssn|(\\d{3}-\\d{2}-\\d{4})",
            file_contents.lower(),
        ):
            has_ssn = True

        if has_ssn:
            storefile(file)

    f.close


def displayfiles():
    for file in flagged_files:
        print(file)


def storefile(file: str):
    flagged_files.append(file)


def main():
    cwd = os.getcwd()  # get the current working directory
    filelist = []  # creates array
    completefilelist = getfiles(
        cwd, filelist
    )  # fills filelist woth all the files in the current working directory

    print("Files with matching text:")
    processfiles(completefilelist)
    displayfiles()
    open_files = input("Would you like to open these flagged files? (y/n)")

    for file in flagged_files:
        if open_files.lower() == "y":
            subprocess.Popen(["notepad.exe", file])


if __name__ == "__main__":
    main()
