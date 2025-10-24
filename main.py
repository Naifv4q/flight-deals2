from data_manager import DataManager
from flight_search import FlightSearch
from pprint import pprint
import pandas as pd
from notification_manager import NotificationManager

my_flight_search = FlightSearch()

#When we first run the code, it updates the cached files; this is to minimize sheety call requests, so later we can work on the data in the cached sheets, instead of calling sheety everytime we do something with the data.
DataManager().update_users_cached_sheet()
DataManager().update_flights_cached_sheet()

# This part of the code checks if we have an empty iataCode, and if so; it fills it with the correct code, then update the sheety page.
flights_data = pd.read_csv("cached_flights_sheet.csv")
sender = NotificationManager()
if flights_data["iataCode"].isnull().any():
    print("Found missing IATA codes, filling them now...")
    my_flight_search.fill_iataCode()
    flights_data = pd.read_csv("cached_flights_sheet.csv")
    flights_data_to_update = flights_data.to_dict(orient="records")
    DataManager().Update_sheety_flights(flights_data_to_update)


Low_price_flights = my_flight_search.search_for_offers()
if Low_price_flights:
    for flight in Low_price_flights:
        if flight.stops == 0:
            sender.send_email(
                msg=f"Low Price Alert !\nOnly ${flight.price} to fly from {flight.origin_city} to {flight.destination_city}, on {flight.out_date}"
            )
        else:
            sender.send_email(
                msg=f"Low Price Alert !\nOnly ${flight.price} to fly from {flight.origin_city} to {flight.destination_city} with {flight.stops} stops, on {flight.out_date}"
            )