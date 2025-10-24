
class FlightData:
    """This class is responsible for structuring the flights data"""
    def __init__(self,price="N/A", origin_city="N/A", destination_city="N/A",out_date="N/A",return_date="N/A",stops = "N/A"):
        self.price = price
        self.origin_city = origin_city
        self.destination_city = destination_city
        self.out_date = out_date
        self.return_date = return_date
        self.stops = stops

