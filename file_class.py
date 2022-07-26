from os.path import join
from severity_enum import Severity


class File:
    """
    Create File Object
    """

    __slots__ = ["filename", "filepath", "extension", "severity"]

    def __init__(self, file: str, directory: str) -> None:
        self.filename: str = file
        self.filepath: str = join(directory, file)
        self.extension: str = ""
        self.severity: Severity = Severity.green
