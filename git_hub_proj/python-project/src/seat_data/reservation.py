#!usr/bin/python

from dataclasses import dataclass

"""
Reservation Class
By @Paul
"""

@dataclass
class Reservation:
    """
    The Reservation that a user makes. 
     -> A Reservation can be attached to multible seats
     -> A User can make multible Reservations
    """

    userID: str  
    layout_name:str 
    seat_pos:(int,int)    
    reserved_at:str 

    def get_rep_fulltext(self):
        payed_string: str = "been payed fully" if self.payed else "not been payed yet"
        return f"User {self.reserved_by} made a reservation at {self.reserve_time}. The bill has {payed_string}"

if __name__=="__main__":
    r_A = Reservation(reserved_by="<User A>")
    print(r_A)