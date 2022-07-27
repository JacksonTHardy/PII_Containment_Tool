#!/usr/bin/env python

import logging
import re
import subprocess
import tkinter
from datetime import datetime
from os import listdir
from os.path import isdir, isfile, join
from pathlib import Path
from tkinter import filedialog
from rich.table import Table
from rich.console import Console
from file_class import File
from severity_enum import Severity


def getfiles(directory: str, file_folder: list[File]) -> list[File]:
    # print("Current working directory: {0}".format(directory))
    for item in listdir(directory):  # for each file in the listdir
        path: str = join(directory, item)  # concat directory with the file
        if isdir(path):  # determines if path is a existing directory or not
            getfiles(path, file_folder)
        elif isfile(path):  # determines if path exist as a file
            file: File = File(item, directory)
            file_folder.append(file)  # if file exist it adds it to a list of all files
        else:
            print("Error with current directory: {0}".format(path))

    return file_folder  # returns a list of all the file names that exist


def processfiles(file_folder: list[File]) -> None:

    for file in file_folder:
        # saves the file suffix like .txt into ext
        file.extension = Path(file.filepath).suffix
        match file.extension:
            # if the file ends in one of the following extensions
            case ".txt" | ".csv" | ".json" | ".xml":
                scanfile(file)
            case _:
                logging.info(
                    f"This file type is not currently handled| Ext: {file.extension}| File: {file.filepath}"
                )


def scanfile(file: File) -> None:
    with open(file.filepath, "r") as f:
        file_contents: str = f.read()
        if re.search(
            "(\\d{3}-\\d{2}-\\d{4})|(^[A-Z0-9._%+-]+@[A-Z0-9.-]+\\.[A-Z]{2,}$)|^(\\+\\d{1,2}\\s)?\\(?\\d{3}\\)?[\\s.-]\\d{3}[\\s.-]\\d{4}$",
            file_contents.upper(),
        ):
            file.severity = Severity.red

            file.flaggeditems.append("PATTERN(RegEx)")
            logging.critical(
                f"This file contains Private Information| File: {file.filepath}"
            )
        elif re.search(
            "national[\\s_]?id|social[\\s_]?security[\\s_]?number|ssn|email[\\s_]address|e-mail[\\s_]address|phone[\\s_]?number|cell[\\s_]?phone[\\s_]?number",
            file_contents.lower(),
        ):
            file.severity = Severity.yellow
            file.flaggeditems.append("SSN(Hard-coded)")
            logging.error(
                f"This file potentially contains Private Information| File: {file.filepath}"
            )
        else:
            file.severity = Severity.green


def displayfiles(file_folder: list[File]) -> None:
    file_folder.sort(key=lambda x: x.severity.value, reverse=True)
    for file in file_folder:
        if file.severity.value > 0:
            print(f"{file.filename}: {file.severity.name}")


def severity_color(x: int) -> str:
    if x == 2:
        return "\033[1;31;40m Red"
    if x == 1:
        return "\033[1;33;40m Yellow"
    return "\033[1;32;40m Green"


def create_file_data(file_folder: list[File]) -> None:
    table = Table(title="Flagged File Data")
    table.add_column("Severity", justify="left")
    table.add_column("File Path", justify="left", style="blue")
    table.add_column("Flagged Items", justify="left", style="purple")
    for file in file_folder:
        if file.severity.value > 0:
            table.add_row(
                file.severity.name,
                file.filepath,
                ", ".join(file.flaggeditems),
            )

    console = Console()
    console.print(table)


def console_print(file_folder: list[File]):
    print(
        f"Files Flagged | File Count: {len([x for x in file_folder if x.severity.value>0])}"
    )
    displayfiles(file_folder)
    create_file_data(file_folder)

    while True:
        open_files: str = input("Would you like to open these flagged files? (Y/N)")
        if open_files.upper() in ["N", "Y"]:
            break
        else:
            print("That Command is not Recognized")

    if open_files.upper() == "Y":
        for file in file_folder:
            if file.severity.value > 0:
                subprocess.Popen(["notepad.exe", file.filepath])


def main() -> None:
    file_folder: list[File] = []  # creates array
    tkinter.Tk(screenName="PII Containment Tool").withdraw()
    path: str = filedialog.askdirectory(title="PII Containment Tool")
    # fills filelist with all the files in the current working directory
    getfiles(path, file_folder)
    processfiles(file_folder)
    if len([x for x in file_folder if x.severity.value > 0]) != 0:
        console_print(file_folder)
    else:
        print("No Flagged files")


if __name__ == "__main__":
    file_folder: list[str] = []
    flagged_severity: list[object] = []
    now: str = datetime.now().strftime("%d_%m_%Y_%H_%M_%S")
    logging.basicConfig(
        filename=f"log_folder\\fileLog_{now}.log",
        encoding="utf-8",
        level=logging.DEBUG,
    )
    main()
