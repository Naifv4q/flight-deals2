import requests
import os
from dotenv import load_dotenv,set_key
import pandas as pd
from requests.exceptions import HTTPError
from datetime import datetime, timedelta
import time
from flight_data import FlightData


class FlightSearch:
    """This class is responsible for searching flight offers and returning them"""
    load_dotenv()
    def __init__(self):
        self.amadeus_api_key = os.getenv("AMADEUS_API_KEY")
        self.amadeus_api_secret = os.getenv("AMADEUS_API_SECRET")
        self.amadeus_access_token = self.get_access_token()

    

    def search_for_offers(self):
        """This method searches flight offers for cities in the cached sheet"""
        search_url = "https://test.api.amadeus.com/v2/shopping/flight-offers"
        data = pd.read_csv("cached_flights_sheet.csv")
        tomorrow_date = (datetime.today() + timedelta(days=1)).strftime("%Y-%m-%d")
        low_price_flights = []
        for index, row in data.iterrows():
            city = row["city"]
            search_params = {
                "originLocationCode" : "RUH",
                "destinationLocationCode" : row["iataCode"],
                "departureDate" : f"{tomorrow_date}",
                "adults" : 1,
                "nonStop" : "true",
                "currencyCode": "USD"
            }

            flight_search_header = {
                "Authorization" : self.amadeus_access_token
                }
            try:
                print(f"Getting direct flights for {city}...")
                search_response = requests.get(url=search_url,headers=flight_search_header,params=search_params)
                search_response.raise_for_status()
            except HTTPError:
                self.update_access_token()
                flight_search_header = {
                "Authorization" : self.amadeus_access_token
                }
                search_response = requests.get(url=search_url,headers=flight_search_header,params=search_params)
                search_response.raise_for_status()
            print("⭕An Amadeus flight offer search call was made ⭕")
            search_response_data = search_response.json().get("data",[])

            if not search_response_data:
                print(f"No direct flights found for {city}")
                time.sleep(1)
                print(f"Getting Non-direct flights for {city}...")
                non_direct_search_params = {
                "originLocationCode" : "RUH",
                "destinationLocationCode" : row["iataCode"],
                "departureDate" : f"{tomorrow_date}",
                "adults" : 1,
                "nonStop" : "false",
                "currencyCode": "USD"
                }
                try:
                    search_response = requests.get(url=search_url,headers=flight_search_header,params=non_direct_search_params)
                    search_response.raise_for_status()
                except HTTPError:
                    self.update_access_token()
                    flight_search_header = {
                    "Authorization" : self.amadeus_access_token
                    }
                    search_response = requests.get(url=search_url,headers=flight_search_header,params=non_direct_search_params)
                    search_response.raise_for_status()
            print("⭕An Amadeus flight offer search call was made ⭕")
            search_response_data = search_response.json().get("data",[])
            self.flight_stops = search_response.json()["data"][0]["itineraries"][0]["segments"][0]["numberOfStops"]
            if not search_response_data:
                print(f"No flights at all found for {city}")
                continue
                

            flight_price = search_response.json()["data"][0]["price"]["total"]
            flight_destination = search_response.json()["data"][0]["itineraries"][0]["segments"][0]["arrival"]["iataCode"]
            flight_origin = search_response.json()["data"][0]["itineraries"][0]["segments"][0]["departure"]["iataCode"]
            flight_dep_date = search_response.json()["data"][0]["itineraries"][0]["segments"][0]["departure"]["at"].split("T")[0]
            
            if float(flight_price) < row["lowestPrice"]:
                print("🪙🪙🪙 Low Price Alert 🪙🪙🪙")
                flight_data = FlightData(
                    price = float(flight_price),
                    origin_city=flight_origin,
                    destination_city=flight_destination,
                    out_date = flight_dep_date,
                    stops = self.flight_stops,
                )
                low_price_flights.append(flight_data)
                return low_price_flights
            print(f"{city}: ${flight_price}")            



    def get_access_token(self):
        """This method gets the amadeus access token from .env"""
        return os.getenv("AMADEUS_ACCESS_TOKEN")


    def update_access_token(self):
        """When requested, this method updates the amadeus access token to a new valid one"""
        access_token_url = "https://test.api.amadeus.com/v1/security/oauth2/token"
        token_header = {
            "Content-Type" : "application/x-www-form-urlencoded"
        }
        token_data = {
            "grant_type" : "client_credentials",
            "client_id" : self.amadeus_api_key,
            "client_secret" : self.amadeus_api_secret,
        }
        access_token_response = requests.post(url=access_token_url,headers=token_header,data=token_data)
        access_token_response.raise_for_status()
        print("⭕An Amadeus token call was made ⭕")
        updated_access_token = f"{access_token_response.json()["token_type"]} {access_token_response.json()["access_token"]}"
        set_key(dotenv_path=".env",key_to_set="AMADEUS_ACCESS_TOKEN",value_to_set= updated_access_token)
        
        self.amadeus_access_token = updated_access_token

    def fill_iataCode(self):
        """when requested, this method fills the missing iataCodes in the cached file """
        city_search_url = "https://test.api.amadeus.com/v1/reference-data/locations/cities"
        city_search_header = {
            "Authorization" : self.amadeus_access_token
        }
        df = pd.read_csv("cached_flights_sheet.csv")
        for index, row in df.iterrows():
            city = row["city"]
            city_search_param = {
                "keyword" : city
            }

            try:
                city_search_response = requests.get(url=city_search_url,headers=city_search_header,params=city_search_param)
                print("⭕An Amadeus city search call was made ⭕")
                city_search_response.raise_for_status()
            except HTTPError:
                self.update_access_token()
                city_search_header = {
                "Authorization" : self.amadeus_access_token
                }
                city_search_response = requests.get(url=city_search_url,headers=city_search_header,params=city_search_param)
                print("⭕An Amadeus city search call was made ⭕")
                city_search_response.raise_for_status()

            df.loc[index,"iataCode"] = city_search_response.json()["data"][0]["iataCode"]
        df.to_csv("cached_flights_sheet.csv",index=False)
        






