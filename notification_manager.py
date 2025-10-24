import os
from dotenv import load_dotenv
import smtplib
import pandas as pd

class NotificationManager:
    """This class is responsible for sending emails to customers when an flight offer have been found"""
    def __init__(self):
        load_dotenv()
        self.my_email = os.getenv("MY_EMAIL")
        self.my_pass = os.getenv("MY_PASS")
        self.cached_user_data = pd.read_csv("cached_users_sheet.csv")
        


    def send_email(self, msg):
        for index ,customer in self.cached_user_data.iterrows():
            customer_name = f"{customer["firstName"]} {customer["lastName"]}"
            with smtplib.SMTP("smtp.gmail.com") as connection:
                connection.starttls()
                connection.login(user=self.my_email, password=self.my_pass)
                connection.sendmail(
                    from_addr=self.my_email,
                    to_addrs=customer["email"],
                    msg=f"Subject:New Low Price Flight!\n\n{customer_name} {msg}".encode('utf-8')
                )



