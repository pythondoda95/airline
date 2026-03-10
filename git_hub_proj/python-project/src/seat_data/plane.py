#!usr/bin/python

from dataclasses import dataclass
from typing import Tuple, List, Set, Optional
from collections.abc import Iterable

from util.logger import Logger
from util.system_tool import SysTools

from seat_data.reservation import Reservation
from seat_data.seat import EconomySeat, BusinessSeat,FirstClassSeat, Seat

from file_handling.loading_configs import (load_seat_config)
from file_handling.reservation_database import ReservationDatabase

from login.database import DatabaseManager
"""
Plane Data Structure, now directly contains the Seat Layout as a value field 
By @Paul, Some Changes by @Felix 
"""

class PlaneInitError(Exception):
    """Raised if the plane initialization fails."""
    def __init__(self, message):
        self.message = message


class Plane:
    """
    Container to store SeatLayout using new seattypes and run methods on it
    Calls the Filereading in its creator
    By @Felix and @Paul
    """

    def __init__(self, seat_layout_file: str):
        """Initializes the object.

        name -- The name of the plane.
        seat_layout_file -- Path to the file describing the plane's seat layout without file extension
        meta_data -- Saves range where classes start and end (seats)
        Raises PlaneInitError, e.g. if the seat layout file is invalid.
        """
        self.name = seat_layout_file
        # Seat Data 
        self.seats = load_seat_config(seat_layout_file+".txt")
        # Other
        self._terminal_width = SysTools.get_terminal_width()
        self.logger = Logger()
        # Reservation Handling 
        self._reservations:List[Reservation] = None
        self._reservations_appended:bool = False 


    def _get_all_user_reservations(self, use_seat_appending:bool = True, always_research:bool = True) -> List[Reservation]:
        """Get all Reservations from the reservations db"""
        if always_research or self._reservations == None: 
            rDB = ReservationDatabase()
            r_raw = rDB.get_all_reservations() # List of [userID, layout_name, seat, reserved_at]
            
            self._reservations = []

            # Attempt to parse new data 
            try:
                for res in r_raw:
                    userID, layout_name, seat_str, reserved_at = res
                    seat_pos = list(map(int, seat_str.split(":")))  # We'll just assume that this works.
                    self._reservations.append(Reservation(userID, layout_name, seat_pos, reserved_at))
            except Exception as e:
                self.logger.error(f"Failed to parse reservation with error: {e}")
        
        if use_seat_appending and (not self._reservations_appended or always_research):
            self.__append_reservation_to_seat()
        
        return self._reservations
                
    def __append_reservation_to_seat(self):
        """
        Adds a Reservation object to all seats for easy Checking
        Do not call from outside the plane.py file 
        """
        if not self._reservations:
            return #Reservations are empty
        if not self._reservations:
            return #Reservations are empty
        for res in self._reservations:
            pos = res.seat_pos
            self.seats[pos[0]][pos[1]].reservation = res 
                
    def get_user_reservations(self, uid) -> List[str]:
        """Return the seats reserved by a user. Formatted as "Row:Column".
        
        uid -- The user's ID
        """
        rDB = ReservationDatabase()
        rows = rDB.get_reservation_for_plane(uid, self.name)

        reservations = []
        for row in rows:
            _userID, _layout_name, seat, _reserved_at = row
            reservations.append(seat)

        return reservations

    def make_reservation(self, seat_coords: str, uid: str):
        """Makes a reservation for a user.

        seat_coords -- The coordinate representation of the seat.

        Raises ValueError if the argument does not represent a seat
        that can be reserved.
        """

        self._get_all_user_reservations() # Load newest Reservation results

        parts = seat_coords.split(":")
        if len(parts) != 2:
            raise ValueError
        
        try:
            row = int(parts[0])
            col = int(parts[1])
        except ValueError:
            # Parsing error
            raise ValueError

        try:
            seat = self.seats[row][col]
        except IndexError:
            raise ValueError

        if seat.reservation is None:
            rDB = ReservationDatabase()
            rDB.reserve_seat(uid, self.name, seat_coords)
        else:
            # Seat is already reserved.
            raise ValueError


    def cancel_reservation(self, seat_coords: str):
        """Cancels the reservation for a seat.

        seat_coords -- The coordinate representation of the seat.

        Raises ValueError if the argument does not represent a seat
        that is currently reserved.
        """

        self._get_all_user_reservations() # Load newest Reservation results

        # NOTE This functions assumes that the legal validation is done before calling. It only checks existance and handles reservation
        coord_tuple = list(map(int, seat_coords.split(":"))) #e.g. 14:5 -> 14,5 Row 5, column 5
        try:
            seat = self.seats[coord_tuple[0]][coord_tuple[1]]
        except IndexError:
            raise ValueError("Seat is outside the plane...")

        self.logger.debug(f"Seat Reservation to cancel: {seat.reservation}") 
        if not seat.reservation:
            raise ValueError("Seat is not reserved")
        else:
            rDB = ReservationDatabase()
            rDB.cancel_any_seat(self.name, seat_coords)
            row, col = coord_tuple
            self.seats[row][col].reservation = None


    # ---- Seat Data Getter START --- #
    def get_seats_raw(self) -> dict: 
        """ Get dict with list of seats for each type"""
        # Seat Type Counting (Can be avoided and done using list slicing if meta data exists)

        flat_list = [item for row in self.seats for item in row]

        economy = [seat for seat in flat_list if isinstance(seat, EconomySeat)]
        buisness = [seat for seat in flat_list if isinstance(seat, BusinessSeat)] 
        first = [seat for seat in flat_list if isinstance(seat, FirstClassSeat)]
        total = economy + buisness + first
        
        self._get_all_user_reservations() # Load newest Reservation results

        economy_reserved = list(filter(lambda x: x.reservation != None, economy))
        buisness_reserved = list(filter(lambda x: x.reservation != None, buisness))
        first_reserved = list(filter(lambda x: x.reservation != None, first))

        reserved = economy_reserved + buisness_reserved + first_reserved
       
        seat_raw = {
            "economy" : economy,
            "buisness" : buisness,
            "first" : first,
            "economy_reserved" : economy_reserved,
            "buisness_reserved" : buisness_reserved,
            "first_reserved" : first_reserved,
            "total" : total,
            "reserved" : reserved 
        }

        return seat_raw

    def get_seat_counts(self) -> dict: 
        """Get dict with count for each seat type (normal and reserved)"""
        seat_raw = self.get_seats_raw()
        seat_count = {
            "economy_count" : len(seat_raw.get("economy") ) ,
            "buisness_count" : len(seat_raw.get("buisness") ) ,
            "first_count" : len(seat_raw.get("first") ) ,
            "economy_reserved_count" : len(seat_raw.get("economy_reserved") ) ,
            "buisness_reserved_count" : len(seat_raw.get("buisness_reserved") ) ,
            "first_reserved_count" : len(seat_raw.get("first_reserved") ) ,
            "total_count" : len(seat_raw.get("total") ) ,
            "reserved_count" : len(seat_raw.get("reserved") )
        }
        return seat_count

    def get_seat_percantages(self) -> dict:
        """ Gets percantage of seat values"""
        seat_counts = self.get_seat_counts()
        # NOTE Need to do something like this to avoid Division by zero error
        if seat_counts.get("economy_reserved_count") > 0:
            economy_ratio = seat_counts.get("economy_count") / seat_counts.get("economy_reserved_count")
        else: 
            economy_ratio = 0
        if seat_counts.get("economy_reserved_count") > 0:
            buisness_ratio= seat_counts.get("buisness_count") / seat_counts.get("buisness_reserved_count")
        else:
            buisness_ratio = 0
        if seat_counts.get("first_reserved_count") > 0:
            first_ratio = seat_counts.get("first_count") / seat_counts.get("first_reserved_count")
        else:
            first_ratio = 0
        if seat_counts.get("economy_reserved_count") > 0:
            total_ratio = seat_counts.get("total_count") / seat_counts.get("reserved_count")
        else:
            total_ratio = 0


        seat_count_percantage = {
            "economy_ratio" : economy_ratio,
            "buisness_ratio" : buisness_ratio,
            "first_ratio" : first_ratio,
            "total_ratio" :  total_ratio
        }

        return seat_count_percantage
    # ---- Seat Data Getter END --- #

    def get_customer(self) -> set:
        """ Get a list of all customer (full data, without pw) that booked at least on seat on the plane"""
        customer_full = []
        user_db_manager = DatabaseManager()
        for user in self._get_customer_userID():
            customer_full.append(user_db_manager.get_user_data(user))
        return customer_full

    def _get_customer_userID(self) -> set:
        """ Get a list of all customer userID that booked at least on seat on the plane"""
        self._get_all_user_reservations() # Load newest Reservation results
        customer:set = []
        if self._reservations:
            for res in self._reservations:
                customer.add(res.userID)
        return customer


    def render_as_text(self, rep_has_reserved:bool = False) -> str:
        """
        Renders the seats as text with reserved seats being represented by 'X'.
        @rep_has_reserved True if the rep char for the seat contains X for taken, default False
        """
        if not self.seats:
            self.logger.warn("The Config appears to be empty")
        
        self._get_all_user_reservations() # Load newest Reservation results

        rows = []
        if rep_has_reserved:
            for row in self.seats:
                row_str = " ".join(("X" if seat.reservation else str(seat)) if seat else "||" for seat in row)
                rows.append(row_str)
        else:
            for row in self.seats:
                row_str = " ".join(str(seat) if seat else "||" for seat in row)
                rows.append(row_str)
        return "\n".join(rows)
    
    def display_full_info(self, display_padding:bool = True) -> str:
        """
        String Rep of the entire plane and all its contained data
        @display_padding - Enable to display ==== Padding. Good for Terminal display, gets disabled for pdf creation 
        """
        # NOTE: Formatting is sometimes somewhat off. It is unclear why

        terminal_width = 80  # Default fallback
        try:
            terminal_width = SysTools.get_terminal_width()
        except:
            pass

        if display_padding:
            padding_name = "=" * ((terminal_width - len(self.name) -2) // 2)
            padding_full = "=" * terminal_width
        else:
            padding_name = ""
            padding_full = ""

        full_display = f"""
        {padding_name}*{self.name}*{padding_name}
        {self.render_as_text()}
        {padding_full}
        {self.__dict_to_str(self.get_seats_raw(), "Raw")}\n
        {self.__dict_to_str(self.get_seat_counts(), "Count")}\n
        {self.__dict_to_str(self.get_seat_percantages(), "Ratios")}\n
        {padding_full}

        """

        return full_display

    def __dict_to_str(self, data:dict, name:str="dictinary") -> str:
        """ 
        Convert a dict to a nice looking string
        - Calls str() on Iterable ELemetns 
        - Gets Position Tupel from Seat Type ELements in Iterables 
        """
        if not data or data == {}:
            self.logger.debug("Dict ist empty or null")
            return "NO DATA - THIS SHOULD NOT BE THE CASE UNLESS PLANE CONFIG IS EMPTY"
        out_list:list = []
        out_list.append(name)
        for key, value in data.items():
            if isinstance(value, Iterable) and type(value) != str:
                if len(value) > 0 and isinstance(value[0], Seat):
                    out_list.append((f" - {key:10} : {[x.position for x in value]}"))
                else:
                    out_list.append((f" - {key:10} : {[str(x) for x in value]}"))
            else:
                out_list.append((f" - {key:10} : {value}"))
        return "\n".join(out_list)
