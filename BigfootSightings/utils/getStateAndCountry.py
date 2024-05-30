from geopy.geocoders import Nominatim
import pandas as pd

#initialize Nominatim API
geolocator = Nominatim(user_agent="BigfootSightings")

LOCAL_PATH = "C:/Users/victo/Desktop/Uni/FemteAar/DIS/BigfootSightings"
CLOSEST_TO_PATH = LOCAL_PATH + "/dataset/archive/HappensAt.csv"

closestToFile = pd.read_csv(CLOSEST_TO_PATH, sep=';', dtype=str)

def getState(lat,lon):
    try:    
        location = geolocator.reverse("{}, {}".format(lat,lon),exactly_one=True)
        address = location.raw['address']
        state = address.get('state','')
        return state
    except:
        return None

def getCountry(lat, lon):
    try:    
        location = geolocator.reverse("{}, {}".format(lat,lon),exactly_one=True)
        address = location.raw['address']
        country = address.get('country','')
        return country
    except:
        return None
    
def getStateAndCountry(lat,lon):
    try:
        location = geolocator.reverse("{}, {}".format(lat,lon),exactly_one=True)
        address = location.raw['address']
        state = address.get('state','')
        country = address.get('country','')
        return country
    except:
        return None

print(getState(49.576457,-98.182798))
print(getCountry(49.576457,-98.182798))

closestToFile['stateName'] = closestToFile.apply(lambda x: getState(x['lat'], x['lng']), axis=1)
closestToFile['country'] = closestToFile.apply(lambda x: getCountry(x['lat'], x['lng']), axis=1)

closestToFile.to_csv('output.csv')
