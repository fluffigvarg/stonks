'''
Simple program meant to automatically update stock prices and changes based on a defined interval.
'''

from yahoo_fin import stock_info as si 
import time
import schedule
from datetime import datetime
from termcolor import colored

class StockTicker:
    def __init__(self, stock_name, moon_price=None): 
        self.stock_name = stock_name
        self.initial_price = 0
        self.current_price = 0
        self.moon_price = moon_price # Target price for alerts
        self.delta = 0
        self.percent_change = 0
        self.text_color = ""

    def ShowLivePrices(self):
        current_time = datetime.now()
        current_time = current_time.strftime("%I:%M:%S %p")
        self.current_price = (si.get_live_price(self.stock_name))
        self.delta = self.current_price - self.initial_price
        self.percent_change = self.delta / self.initial_price
        self.percent_change *= 100

        if self.delta > 0:
            self.text_color = "green"
        elif self.delta < 0:
            self.text_color = "red"
        else: 
            self.text_color = "white"
        
        print(colored(f"{self.stock_name}: Current ${self.current_price:.2f} (${self.delta:.2f} {self.percent_change:.2f}%) | Initial ${self.initial_price:.2f} | {current_time}", self.text_color))
    
    def Alerts(self): 
        # Alerts for target prices, a.k.a. Moon Price
        if self.moon_price:
            if self.current_price > self.moon_price:
                print(colored("--------------------------", "green"))
                print(colored(f"Pay attention to {self.stock_name}! It's going to the moon!", "green"))
                print(colored("--------------------------", "green"))

            if self.current_price > (self.moon_price * .5):
                print(colored("--------------------------", "yellow"))
                print(colored(f"{self.stock_name} is half way to the moon!", "yellow"))
                print(colored("--------------------------", "yellow"))

    def InitialPrice(self):
        self.initial_price = (si.get_live_price(self.stock_name))

# How often you want to update prices (currently in seconds)
update_time = 600

# Create objects for each stock you want to track ("Ticker Symbol", Moon Price)
gme = StockTicker("GME", 1000)
amc = StockTicker("AMC", 40)

# Add stock objects here
stonks = [gme, amc]

# Grab price at launch of app for a reference point
for stonk in stonks:
    stonk.InitialPrice()

# Just an intro message
print(f"Fueling up the rocket, please be patient...will take about {update_time} seconds...")

# Check live price and alert to swings
for stonk in stonks:
    schedule.every(update_time).seconds.do(stonk.ShowLivePrices)
    schedule.every(update_time).seconds.do(stonk.Alerts)

# Used for timer
while True:
    schedule.run_pending()
    time.sleep(1)