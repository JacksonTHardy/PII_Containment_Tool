# PII_Containment_Tool


## Description
Detects Personally Identifiable Information (PII) within a working directory. Allows the user to view files.

## Requirements
- Python >= 3.10
- Other Requirements are found in `Requirements.txt`
- To install, use the below command in the Terminal
```python
python -m pip install -r requirements.txt
```

## TODO
### Base Functionality
- [X] Scan directory for files
- [X] Filter for certain file extensions
    - [X] .txt
    - [X] .csv
    - [X] .json
    - [X] .xml
    - [ ] .pdf
    - [ ] .xlsx
- [X] Read files for PII
    - [X] Social Security Number
        - [X] Field Headers
        - [X] Regex values
    - [ ] Address Data
    - [ ] Name Data 
    - [X] Email
        - [X] Field Headers
        - [X] Regex values
    - [X] Phone Number
        - [X] Field Headers
        - [X] Regex values
    - [ ] IDs
- [ ] Options for handling Flagged Files
    - [ ] Delete File
    - [ ] Ignore
    - [ ] Mask Data
    - [ ] Manual Update
- [X] Intensity Levels for flagged files
### User Interface
- [X] Command Line Tool
- [X] Open Files For Review
- [X] Open File Explorer for Directory Selection
- [ ] Full UI 
