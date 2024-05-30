import os
import pandas as pd

# this is needed to imprt app.py from the parent directory (K.V.)
import sys
import os.path

# Add the parent directory to the system path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import app

LOCAL_PATH = "C:\\Users\\victo\\Desktop\\Uni\\FemteAar\\DIS/BigfootSightings"
SIGHTINGS_PATH = LOCAL_PATH + "/dataset/archive/Sightings.csv"
HAPPENS_AT_PATH = LOCAL_PATH + "/dataset/archive/HappensAt.csv"
LOCATIONS_PATH = LOCAL_PATH + "/dataset/archive/Locations.csv"

def get_label_name(string):
    return string.replace("_", " ").capitalize()


class ModelChoices:
    def __init__(self, choices_list):
        for item in choices_list:
            setattr(self, item.lower(), get_label_name(item))

    def choices(self):
        return [(k, v) for k, v in self.__dict__.items()]

    def values(self):
        return [v for v in self.__dict__.keys()]

    def labels(self):
        return [l for l in self.__dict__.values()]


sightingsFile = pd.read_csv(SIGHTINGS_PATH, sep=';', dtype=str)
locationsFile = pd.read_csv(LOCATIONS_PATH, sep=';', dtype=str)
happensAtFile = pd.read_csv(HAPPENS_AT_PATH, sep=';', dtype=str)

print("DATA_READ:")
print(sightingsFile)
print("DATA_READ:")
print(locationsFile)
print("DATA_READ:")
print(happensAtFile)


SightingNumber = ModelChoices(sightingsFile.number.unique())
SightingTitle = ModelChoices(sightingsFile.title)
SightingTime = ModelChoices(sightingsFile.timestamp)

locationLat = ModelChoices(locationsFile.lat)
locationLng = ModelChoices(locationsFile.lng)
locationState = ModelChoices(locationsFile.stateName)
locationCountry = ModelChoices(locationsFile.country)

happensAtNr = ModelChoices(happensAtFile.number)
happensAtLat = ModelChoices(happensAtFile.lat)
happensAtLng = ModelChoices(happensAtFile.lng)