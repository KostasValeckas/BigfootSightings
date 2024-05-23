import os
import pandas as pd

# this is needed to imprt app.py from the parent directory (K.V.)
import sys
import os.path

# Add the parent directory to the system path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import app



SIGHTINGS_PATH = "/home/kostasvaleckas/Documents/DIS/Victor_cities_data/BigfootSightings-main/dataset/archive/bfro_locations.csv"
CITIES_PATH = "/home/kostasvaleckas/Documents/DIS/Victor_cities_data/BigfootSightings-main/dataset/archive/Cities.csv"

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


sightingsFile = pd.read_csv(SIGHTINGS_PATH, sep=',', dtype=str)
citiesFile = pd.read_csv(CITIES_PATH, sep=';', dtype=str)

print("DATA_READ:")
print(sightingsFile)
print("DATA_READ:")
print(citiesFile)

SightingNumber = ModelChoices(sightingsFile.number.unique())
SightingTitle = ModelChoices(sightingsFile.title.unique())
SightingLat = ModelChoices(sightingsFile.latitude)
SightingLong = ModelChoices(sightingsFile.longitude)

CityName = ModelChoices(citiesFile.cityName)
StateID = ModelChoices(citiesFile.stateID)
StateName = ModelChoices(citiesFile.stateName)
Country = ModelChoices(citiesFile.country)
