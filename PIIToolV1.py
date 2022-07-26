#!/usr/bin/env python

# Import the os module
# import os
# from ctypes import sizeof

import logging
import re
import subprocess
import tkinter
from datetime import datetime
from os import listdir
from os.path import isdir, isfile, join, exists
from pathlib import Path
from tkinter import filedialog
from severity_enum import Severity


def getfiles(directory: str, filelist: list[str]) -> list[str]:
    # print("Current working directory: {0}".format(directory))
    for file in listdir(directory):  # for each file in the listdir
        path: str = join(directory, file)  # concat directory with the file
        if isdir(path):  # determines if path is a existing directory or not
            getfiles(path, filelist)
        elif isfile(path):  # determines if path exist as a file
            filelist.append(path)  # if file exist it adds it to a list of all files
        else:
            print("Error with current directory: {0}".format(path))

    return filelist  # returns a list of all the file names that exist


def processfiles(completefilelist: list[str]) -> None:
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
            case _:
                logging.info(
                    f"This file type is not currently handled| Ext: {ext}| File: {file}"
                )


def scanfile(file: str) -> None:
    with open(file, "r") as f:
        file_contents: str = f.read()
        if re.search(
            "national[\\s_]?id|social[\\s_]?security[\\s_]?number|ssn|(\\d{3}-\\d{2}-\\d{4})",
            file_contents.lower(),
        ):
            storefile(file)
            process_severity(file_contents)


def displayfiles() -> None:
    for file in flagged_files:
        print(file)


def storefile(file: str) -> None:
    flagged_files.append(file)


def process_severity(contents: str) -> None:
    if re.search("(\\d{3}-\\d{2}-\\d{4})", contents):
        flagged_severity.append(Severity.red)
    elif re.search(
        "national[\\s_]?id|social[\\s_]?security[\\s_]?number|ssn", contents.lower()
    ):
        flagged_severity.append(Severity.yellow)
    else:
        flagged_severity.append(Severity.green)


def find_next_path(filepath: str) -> str:
    i: int = 0
    while exists(filepath):
        i += 1
        if i > 1:
            filepath = filepath[0 : len(filepath) - 1]
        filepath += str(i)
    return filepath


def create_file_data(filepath: str) -> None:
    counter: int = 0
    with open(
        find_next_path(filepath + "flaggedFileData"),
        "w",
    ) as f:
        for file in flagged_files:
            f.write(file)
            f.write(flagged_severity[counter].__str__() + "\n")
            counter += 1
    f.close()


def main() -> None:
    filelist: list[str] = []  # creates array
    tkinter.Tk(screenName="PII Containment Tool").withdraw()
    path: str = filedialog.askdirectory(title="PII Containment Tool")
    completefilelist: list[str] = getfiles(
        path, filelist
    )  # fills filelist with all the files in the current working directory

    processfiles(completefilelist)
    if len(flagged_files) != 0:
        print(f"Files Flagged | File Count: {len(flagged_files)}")
        displayfiles()
        print("\n")
        print(flagged_severity)
        create_file_data("Flagged_file_data_Log")

        while True:
            open_files: str = input("Would you like to open these flagged files? (Y/N)")
            if open_files.upper() in ["N", "Y"]:
                break
            else:
                print("That Command is not Recognized")

        if open_files.upper() == "Y":
            for file in flagged_files:
                subprocess.Popen(["notepad.exe", file])
    else:
        print("No Flagged files")


if __name__ == "__main__":
    global flagged_files
    flagged_files: list[str] = []
    global flagged_severity
    flagged_severity: list[object] = []
    now: str = datetime.now().strftime("%d_%m_%Y_%H_%M_%S")
    logging.basicConfig(
        filename=f"log_folder\\fileLog_{now}.log",
        encoding="utf-8",
        level=logging.DEBUG,
    )
    main()
