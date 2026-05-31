import pandas as pd
import numpy as np
from langchain.tools import tool
from dataclasses import dataclass
import random

airlines = pd.read_csv("backend/data/airlines.csv")
routes = pd.read_csv("backend/data/routes.csv")
airports = pd.read_csv("backend/data/airports.csv")

@dataclass
class Airport:
    name:str
    city:str
    country:str
    id:int

@dataclass
class FlightRoute:
    airline:str
    stops:int
    fromAirport:Airport
    toAirport:Airport
    cost:float #random data as of now in fromCity currency


def getFlightsBetweenAirports(fromAirport:Airport, toAirport:Airport) -> list[FlightRoute]:
    """
    Get all the flight routes running between two airports as a list of FlightRoute object. 
    Returns information about each route which contains airline name, number of stops between source and destination,
    source airport information, destination airport information, cost of the ticket in the currency of the source airport's country.

    IMPORTANT
    DO NOT ADD any additional flight routes
    """

    print(f"--INVOKING getFlightsBetweenAirports tool with from airport {fromAirport.id} and to airport {toAirport.id}")
    result = []
    for _,route in routes[(routes["Source airport ID"].astype(str) == str(fromAirport.id)) & (routes["Destination airport ID"].astype(str) == str(toAirport.id))].iterrows():
        airline = airlines[(airlines["Airline ID"].astype(str) == str(route["Airline ID"])) &(airlines["Active"] == "Y")]
        if not airline.empty:
            result.append(FlightRoute(airline.iloc[0]["Name"], route["Stops"], fromAirport, toAirport, random.randint(1000, 5000)))
    return result
    

@tool
def getAirportsInCityOfCountry(city:str, country:str) -> list[Airport]:
    """Get all the airport names in a particular city of a given country as a list of Airport object
    IMPORTANT
    Do not invent additional airports.
    """
    print(f"--INVOKING getAirportsInCityOfCountry tool with city {city}, country {country}")
    result = []
    for _,airport in airports[(airports["City"].astype(str) == city) & (airports["Country"].astype(str)==country)].iterrows():
        result.append(Airport(airport["Name"], airport["City"], airport["Country"], airport["Airport ID"]))
    return result

@tool
def getAirportsInCity(city:str) -> list[Airport]:
    """Get all the airport names in a particular city list of Airport object
    IMPORTANT
    Do not invent additional airports.
    """
    print(f"--INVOKING getAirportsInCity tool with city {city}")
    result = []
    for _,airport in airports[airports["City"].astype(str) == city].iterrows():
        result.append(Airport(airport["Name"], airport["City"], airport["Country"], airport["Airport ID"]))
    return result

@tool
def getAirportsInCountry(country:str) -> list[Airport]:
    """
    Get all the airport names in a particular country list of Airport object
    IMPORTANT
    Do not invent additional airports.
    """
    print("--INVOKING getAirportsInCountry tool")
    result = []
    for _,airport in airports[airports["Country"].astype(str) == country].iterrows():
        result.append(Airport(airport["Name"], airport["City"], airport["Country"], airport["Airport ID"]))
    return result