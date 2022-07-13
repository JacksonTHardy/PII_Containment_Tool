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
        has_ssn: bool = False
        file_contents: str = f.read()  # Giant if statment below is hard to follow.
        # I had to do it like this because the string literals would not pick up stuff like this <SSN>
        if (
            re.search(
                "[n]+[a]+[t]+[i]+[o]+[n]+[a]+[l]+[ ]+[i]+[d]",
                file_contents.lower(),
            )
            or re.search("[s]+[s]+[n]", file_contents.lower())
            or re.search(
                "[s]+[o]+[c]+[i]+[a]+[l]+[ ]+[s]+[e]+[c]+[u]+[r]+[i]+[t]+[y]+[ ]+[n]+[u]+[m]+[b]+[e]+[r]",
                file_contents.lower(),
            )
            or re.search("(\\d{3}-\\d{2}-\\d{4})", file_contents) is not None
        ):
            has_ssn = True

        if has_ssn is True:
            print(file)
        """commented out stuff is another solution than the one above
        for line in f:  # for each line in the file
            if (
                "ssn" or "social security number" or "national id"
            ) in line.lower():  # check for hard coded strings in the file
                has_ssn = True

        f.seek(0)  # reset the file position back to the beginning

        social_found = re.search(
            "(\\d{3}-\\d{2}-\\d{4})", f.read()
        )  # search for this specific pattern

        if (
            social_found is not None or has_ssn
        ):  # if file is flagged print the file name
            print(file)
        """

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
