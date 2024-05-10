import os
import pandas as pd

# this is needed to imprt app.py from the parent directory (K.V.)
import sys
import os.path

# Add the parent directory to the system path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import app



DATASET_PATH = "/home/kostasvaleckas/Documents/DIS/Project_Sketch/BigfootSightings/dataset/archive/bfro_locations.csv"


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


df = pd.read_csv(DATASET_PATH, sep=',', dtype=str)

print("DATA_READ:")
print(df)

SightingNumber = ModelChoices(df.number.unique())
SightingTitle = ModelChoices(df.title.unique())
SightingLat = ModelChoices(df.latitude.unique())
SightingLong = ModelChoices(df.longitude.unique())
