import requests
from dotenv import load_dotenv
import os
from requests.exceptions import HTTPError
from pandas.errors import EmptyDataError
import pandas as pd

class DataManager:
    """This class is responsible for managing the data of the whole project, from flights to users."""
    def __init__(self):
        load_dotenv()
        self.Sheety_auth = os.getenv("SHEETY_AUTH")
        self.sheety_header = {
            "Authorization": self.Sheety_auth
        }
        try:
            self.flights_sheet_data = pd.read_csv("cached_flights_sheet.csv")
        except EmptyDataError:
            self.flights_sheet_data = self.update_flights_cached_sheet()
        
        
    def get_users_sheet_data(self):
        """Returns the latest users sheet data from google sheets"""
        sheety_users_url = "https://api.sheety.co/1eec04094d159e8e9210c1989efc2933/myFlightDeals/users"
        try:
            sheety_response = requests.get(url=sheety_users_url,headers=self.sheety_header)
            sheety_response.raise_for_status()
            print("⭕A sheety get call was made ⭕")
        except HTTPError:
            print("Sheety users sheet call was unsuccessful !")
        users_sheet_data = sheety_response.json()["users"]
        return users_sheet_data
    
    def update_users_cached_sheet(self):
        """Updates the cached sheet to the latest data from google sheets"""
        try:
            pd.DataFrame().to_csv("cached_users_sheet.csv",index=False)
            data = self.get_users_sheet_data()
            df = pd.DataFrame(data)
            df.to_csv("cached_users_sheet.csv",index=False)
        except EmptyDataError:
            data = self.get_users_sheet_data()
            df = pd.DataFrame(data)
            df.to_csv("cached_users_sheet.csv",index=False)

    #Note: We dont update the sheety users data like flights, because from this side we only read the users data, and not modify, or update them like flights when they get cheaper.

    def get_flights_sheet_data(self):
        """Returns the latest flights sheet data from google sheets"""
        sheety_flights_url = "https://api.sheety.co/1eec04094d159e8e9210c1989efc2933/myFlightDeals/prices"
        try:
            sheety_response = requests.get(url=sheety_flights_url,headers=self.sheety_header)
            sheety_response.raise_for_status()
            print("⭕A sheety get call was made ⭕")
        except HTTPError:
            print("Sheety flight sheet call was unsuccessful !")
        flights_sheet_data = sheety_response.json()["prices"]
        return flights_sheet_data
    
    def update_flights_cached_sheet(self):
        """Updates the cached sheet to the latest data from google sheets"""
        try:
            pd.DataFrame().to_csv("cached_flights_sheet.csv",index=False)
            data = self.get_flights_sheet_data()
            df = pd.DataFrame(data)
            df.to_csv("cached_flights_sheet.csv",index=False)
        except EmptyDataError:
            data = self.get_flights_sheet_data()
            df = pd.DataFrame(data)
            df.to_csv("cached_flights_sheet.csv",index=False)

    def Update_sheety_flights(self,data):
        """Updates the google sheets with our cached data"""
        update_url = "https://api.sheety.co/1eec04094d159e8e9210c1989efc2933/myFlightDeals/prices/"
        for row in data:
            row_id = row["id"]
            update_payload = {
                "price" : row
            }
            sheety_update_response = requests.put(url=f"{update_url}{row_id}",headers=self.sheety_header,json=update_payload)
            print("⭕A sheety put call was made ⭕")

            sheety_update_response.raise_for_status()
            print("Succesfully updated a row in the sheet !")
        latest_data = self.get_flights_sheet_data()
        df = pd.DataFrame(latest_data)
        df.to_csv("cached_flights_sheet.csv",index=False)
        
