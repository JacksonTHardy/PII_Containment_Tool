#!/usr/bin/env python

# Import the os module
import os
from os import listdir
from os.path import isfile, isdir, join
from pathlib import Path
import re


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
    for file in completefilelist:
        ext: str = Path(file).suffix  # saves the file suffix like .txt into ext
        match ext:
            case ".txt" | ".csv" | ".json" | ".xml":  # if the file ends in one of the following extensions
                scanfile(file)


def scanfile(file: str):
    with open(file, "r") as f:
        SSN: str = "ssn"
        social_security_number: str = "social security number"
        national_id: str = "national id"
        has_ssn: bool = False
        for line in f:  # for each line in the file
            if (
                SSN and social_security_number and national_id in line.lower()
            ):  # check for hard coded strings in the file
                has_ssn = True

        f.seek(0)  # reset the file position back to the beginning
        social_found = re.search(
            "(\\d{3}-\\d{2}-\\d{4})", f.read()
        )  # search for this specific pattern
        if (
            social_found is not None or has_ssn is True
        ):  # if file is flagged print the file name
            print(file)
            has_ssn = False
        f.close


def main():
    cwd = os.getcwd()  # get the current working directory
    filelist = []  # creates array
    completefilelist = getfiles(
        cwd, filelist
    )  # fills filelist woth all the files in the current working directory

    print("Files with matching text:")
    processfiles(completefilelist)


if __name__ == "__main__":
    main()
