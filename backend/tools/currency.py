from dotenv import load_dotenv
from langchain.tools import tool
import requests
import pandas as pd
import os

load_dotenv()


def exchageRate(country1:str, country2:str) -> float:
    """Gets the value of 1 unit of country1's currency in country2's currency. country1 and country2 is the country name"""   
    df = pd.read_csv("data/currency.csv")

    print("----INVOKING AGENT exchange rate with params ", country1, country2)

    currencyOfCountry1 = df[df["Country"] == country1].iloc[0]
    currencyOfCountry2 = df[df["Country"] == country2].iloc[0]

    currencyCodeOfCountry1 = currencyOfCountry1["Currency Code"]
    currencyNameOfCountry1 = currencyOfCountry1["Currency Name"]

    currencyCodeOfCountry2 = currencyOfCountry2["Currency Code"]
    currencyNameOfCountry2 = currencyOfCountry2["Currency Name"]

    url = "https://v6.exchangerate-api.com/v6/" + os.getenv("EXCHANGE_RATE_API") + "/latest/" + currencyCodeOfCountry1
    
    response = requests.get(url).json()
    value = response.get("conversion_rates").get(currencyCodeOfCountry2)
    return f"1 {currencyNameOfCountry1} is {value} of {currencyNameOfCountry2}" 