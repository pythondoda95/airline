import numpy as np 
import matplotlib as mpl 
import matplotlib.pyplot as plt 

from typing import Dict, List, Optional, Union

from seat_data.plane import Plane
from seat_data.price_data import PricingConfig
from util.logger import Logger
from statistics.chart_handler import ChartCreator
from file_handling.reservation_database import ReservationDatabase

class PlaneChartCreations():
    def __init__(self, plane:Plane):
        self.plane = plane 
        self.cc = ChartCreator()
        self.logger = Logger()
    
    def create_all_charts(self):
        """ Creates all Charts available with their respective default names and parameters"""
        # NOTE Weird looking try-catch blob to still get some through if one fails for some reason 
        try:
            self.seat_types_bar()
        except Exception as a:
            self.logger.error(f"Failed to create chart Number 1 {a}") 
        try:
            self.seat_types_ratio_pie() 
        except Exception as a:
            self.logger.error(f"Failed to create chart Number 2.", a) 
        try:
            self.seat_type_reserved_compare_bar() 
        except Exception as a:
            self.logger.error(f"Failed to create chart Number 3 {a}") 
        try: 
           self.reserved_total_pie() 
        except Exception as a:
           self.logger.error(f"Failed to create chart Number 4.", a)
        try:
            self.reservations_per_user_line() 
        except Exception as a:
            self.logger.error(f"Failed to create chart Number 5 {a}")

    # Number 1
    def seat_types_bar(self):
        """ Bar chart of different seat types. (Does not look at reservation stuff)"""
        data_raw:dict = self.plane.get_seat_counts()
        data_cleaned: dict = dict(list(data_raw.items())[:3])

        self.cc.plot_data(
            plot_type= "bar",
            data= data_cleaned,
            x_label= "Seat Category",
            y_label= "Seat Count",
            title= "Seat Count by Seating Class",
            file_name = "seat_types_bar",
        )

    # Number 2
    def seat_types_ratio_pie(self):
        """ Ratio of Seat Types to each other """
        data_raw:dict = self.plane.get_seat_counts()
        data_cleaned: dict = dict(list(data_raw.items())[:3])
        self.logger.debug(f"Data Cleaned 2:\n{data_cleaned}")

        self.cc.plot_data(
            plot_type= "pie",
            data= list(data_cleaned.values()), # Limitation by CC: Pie INput needs to be a list
            title= "Seat Type Ratio",
            file_name = "seat_types_ratio_pie",
        ) 

    # Number 3
    def seat_type_reserved_compare_bar(self):
        """ Different seat types with reservation side by side each""" 
        data_raw:dict = self.plane.get_seat_counts()
        custom_order:list = ["economy_count", "economy_reserved_count", "buisness_count", "buisness_reserved_count", "first_count", "first_reserved_count"]
        data_cleaned = {k: data_raw[k] for k in custom_order}
        #self.logger.debug(f"Data Cleaned 3:\n{data_cleaned}")

        self.cc.plot_data(
            plot_type= "bar",
            data= data_cleaned,
            x_label= "Seat Category",
            y_label= "Seat Count",
            title= "Seat Count Comparison by Seating Class & Reserved Status",
            file_name = "seat_type_reserved_compare_bar",
        ) 

    # Number 4
    # TODO Remove 
    def reserved_total_pie_old(self):
        """ Pie Chart with two slices (Reserved and not reserved)"""
        try:
            data_raw:dict = self.plane.get_seat_counts()
            reserved:int = data_raw.get("reserved_count")
            free:int = data_raw.get("total_count") - data_raw.get("reserved_count")
            self.logger.debug(f"Data Cleaned 4:\nReserved Count{reserved} Free Count {free}")
        except Exception as e:
            self.logger.error("Something went wrong with data grabber for Chart Creatin 4")

        self.cc.plot_data(
            plot_type= "pie",
            data= [reserved, free],
            title= "Seat Count Reservation Ratio",
            file_name = "reserved_total_pie",
        ) 

    def reserved_total_pie(self):
        """ Pie Chart with two slices (Reserved and not reserved)"""
        data_raw:dict = self.plane.get_seat_counts()
        
        # Handle empty data
        if data_raw["total_count"] == 0:
            self.logger.error("Cannot create pie chart: No seats available")
            return
        
        reserved = data_raw.get("reserved_count", 0)
        free = data_raw.get("total_count", 0) - reserved

        self.cc.plot_data(
            plot_type= "pie",
            data= [reserved, free],
            _labels=["Reserved", "Free"],
            title= "Seat Count Reservation Ratio",
            file_name = "reserved_total_pie",
        ) 
    # Number 5
    def reservations_per_user_line(self):
        """ Line Chart with counts per user on how many seats they reserved"""
        rDB = ReservationDatabase()
        user:set = None 
        # Note: Legacy Try-Catch. Could be removed since the issue is solved
        try:
            user = self.plane._get_customer_userID()
            self.logger.debug(f"5: user: {user}")
            if user:
                user_reservations = {
                    x: len(rDB.get_reservation(x) or [])  
                    for x in user
                }
            else:
                self.logger.warn("No users found, Can't iterate through Empty/None -> Aborting")
                return 
        except Exception as e:
            self.logger.error("Something went wrong with the reservations for Chart Creation 5")
            return 

        self.cc.plot_data(
            plot_type= "line",
            data= user_reservations,
            x_label= "User",
            y_label= "Reservation Count",
            title= "Reservations per User",
            file_name = "reservations_per_user_line",
        ) 