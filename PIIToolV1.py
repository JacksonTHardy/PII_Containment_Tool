#!/usr/bin/env python

# Import the os module
from ast import pattern
from operator import truediv
import os
from os import listdir
from os.path import isfile, isdir, join
from pathlib import Path
import re


def getfiles(directory, filelist):
    # print("Current working directory: {0}".format(directory))

    for file in listdir(directory): # for each file in the listdir
        path = join(directory, file) # concats directory with the file
        if isdir(path): # determines if path is a exsisting directory or not
            filelist = getfiles(path, filelist)
        elif isfile(path): # determines if path exist as a file
            filelist.append(path) # if file exist it adds it to a list of all files
        else:
            print("Error with current directory: {0}".format(path))

    return filelist # returns a list of all the file names that exist


def processfiles(completefilelist):
    fileText = ""
    hasSSN = False
    SSN = "ssn"
    SocialSecurityNumber = "social security number"
    NationalID = "national id"
    #social = re.compile("\d{3}-\d{2}-\d{4}")
    for file in completefilelist:
        ext = Path(file).suffix # saves the file suffix like .txt into ext
        #print(ext)
        match ext:
            case ".txt" | ".csv" | ".json" | ".xml":
                with open(file, "r") as f:
                    #printFileContents(file)
                    for line in f:
                        if SSN in line.lower():
                            hasSSN = True
                        if SocialSecurityNumber in line.lower():
                            hasSSN = True
                        if NationalID in line.lower():
                            hasSSN = True

                    f.seek(0)
                    socialFound = re.search("(\d{3}-\d{2}-\d{4})", f.read())
                    if socialFound != None:
                        print(file)
                    if hasSSN == True:
                        print(file)
                        hasSSN = False
                #scanfile(file, text)
                f.close


#def scanfile(file, text):
 #   with open(file, "r") as f:
  #      if text in f.read(): # if text is in the file f
   #         print(file)

def printFileContents(fileToPrint):
    with open(fileToPrint, "r") as prtFile:
        print(prtFile.readlines())

def main():
    cwd = os.getcwd() # get the current working directory
    filelist = [] # creates array
    completefilelist = getfiles(cwd, filelist) # fills filelist woth all the files in the current working directory

    print("Files with matching text:")
    processfiles(completefilelist)


if __name__ == "__main__":
    main()
