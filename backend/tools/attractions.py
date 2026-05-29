import math
import requests
from langchain.tools import tool
from dataclasses import dataclass
import os

from dotenv import load_dotenv

load_dotenv()

@dataclass
class Attraction:
    name:str #name of the attraction
    rate:int # rating of the attraction
    kinds:list[str] # kind of attraction, can be multiple kinds

@dataclass
class Location:
    lat:float
    long:float

@dataclass
class BoundingBox:
    lat_min: float
    lat_max: float
    lon_min: float
    lon_max: float


@tool
def getNearByAttractions(city:str, radius:float=1.0)->list[Attraction]:
    """Gets nearby attractions, sight seeing locations, must visit places of a given city or country in a given radius(kms). If radius is not give, assume 1km as default
    IMPORTANT:
    Use ONLY the returned attractions when answering the user.
    Do not invent additional attractions.
    Prioritize attractions with higher ratings.
    Group the attractions by kind.
    """

    print("--INVOKING getNearByAttractions tool with params", city, radius)
    coords = get_bounding_box(getCoordinates(city), radius)
    print("co ords ", coords)

    url = f"https://api.opentripmap.com/0.1/en/places/bbox?lon_min={coords.lon_min}&lon_max={coords.lon_max}&lat_min={coords.lat_min}&lat_max={coords.lat_max}&apikey={os.getenv("OPEN_TRIP_API")}"
    response = requests.get(url).json()
    
    listOfAttractions = []
    index = 0
    for attraction in response.get("features"):
        properties = attraction.get("properties")
        listOfAttractions.append(Attraction(properties.get("name"), properties.get("rate"), properties.get("kinds").split(",")))
        index+=1
        if(index == 5):
            break
    return listOfAttractions
    

def getCoordinates(city:str)->Location:
    url = f"https://api.opentripmap.com/0.1/en/places/geoname?name={city}&apikey={os.getenv("OPEN_TRIP_API")}"
    response = requests.get(url).json()
    return Location(response["lat"], response["lon"])


def get_bounding_box(loc:Location, radius_km=1.0)->BoundingBox:
    # Fixed earth conversion factor
    KM_PER_DEGREE_LAT = 111.1
    
    # Calculate delta variations
    delta_lat = radius_km / KM_PER_DEGREE_LAT
    delta_lon = radius_km / (KM_PER_DEGREE_LAT * math.cos(math.radians(loc.lat)))
    
    # Calculate boundaries
    lat_min = loc.lat - delta_lat
    lat_max = loc.lat + delta_lat
    lon_min = loc.long - delta_lon
    lon_max = loc.long + delta_lon
    
    return BoundingBox(lat_min, lat_max, lon_min, lon_max)
