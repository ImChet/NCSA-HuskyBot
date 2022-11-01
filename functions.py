import json
import os
import shutil
from datetime import datetime


# Function Definitions

def getCurrentDateTime():
    return f'{datetime.now().strftime("%m/%d/%Y")} at {(datetime.strptime(datetime.now().strftime("%H:%M:%S"), "%H:%M:%S")).strftime("%r")}'


def removeFilesFromDirectory(working_directory):
    for file in os.scandir(working_directory):
        os.remove(file.path)


def removeDirectory(working_directory):
    shutil.rmtree(working_directory)


def checkDirectoryExists(directory):
    path = directory
    directory_exists = os.path.exists(path)
    if directory_exists is False:
        os.mkdir(path)


def checkDirectoryExistsDelete(directory):
    path = directory
    directory_exists = os.path.exists(path)
    if directory_exists is True:
        shutil.rmtree(path)


def ensureTicketingJSON_Exists():
    filepath = 'WorkingFiles/Databases/TicketingJSON.json'
    file_exists = os.path.exists(filepath)
    if file_exists is False:
        f = open(filepath, "w")
        f.close()


# To lowercase
def to_lower(arg: str):
    return arg.lower()


# To uppercase
def to_upper(arg: str):
    return arg.upper()
