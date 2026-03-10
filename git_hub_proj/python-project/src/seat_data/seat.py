#!usr/bin/python 

from dataclasses import dataclass
from typing import Tuple 

from seat_data.reservation import Reservation

"""
Base Seat Type and its derivativs
By @Paul with Extension by @Irembrar
"""

@dataclass
class Seat:
    """Basic Seat Class"""
    price:int = -1 
    name:str = "Standard Seat"
    char_rep:str = "S"
    reservation:Reservation = None # Gets attached post init in the plane.py (If needet)
    position:tuple[int, int] = None # Gets attached post parsing 
    
    def __repr__(self) -> str:
        return self.char_rep

    def __str__(self) -> str:
        return self.char_rep

    def full_info(self) -> str:
        return f"{self.name} ({self.char_rep}) with price: {self.price}€. Reserved by: {self.reservation}"


# === Actual Seat Classes for Booking ===
# By iremebrar
# Replaces old unused seat structure
@dataclass
class EconomySeat(Seat):
    """Standard economy class seat"""

    def __post_init__(self):
        self.name = "economy"
        if self.char_rep == "S": self.char_rep = "E"
        self.price = 100


@dataclass
class BusinessSeat(Seat):
    """Business class seat"""

    def __post_init__(self):
        self.name = "business"
        if self.char_rep == "S": self.char_rep = "B"
        self.price = 300


@dataclass
class FirstClassSeat(Seat):
    """First class seat"""

    def __post_init__(self):
        self.name = "first"
        if self.char_rep == "S": self.char_rep = "F"
        self.price = 600
