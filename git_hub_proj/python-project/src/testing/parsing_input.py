#!usr/bin/python

from dataclasses import dataclass
from typing import Tuple, List, Optional
from pathlib import Path 

from util.logger import Logger
from util.system_tool import SysTools

from seat_data.plane import SeatLayout, PlaneConfig
from seat_data.seat import Seat 
from seat_data.reservation import Reservation

from file_handling import loading_configs as Loader

# Run Using: python3 -m testing.A

"""
Testing Differnt Parts of the project in a centrall location
TODO: The current file path handling is horrible - Paul
By @Paul
"""

CONFIG_FOLDER = Path(__file__).parent.parent.parent / "seat_configs"
LAYOUT_FILE_NAME= CONFIG_FOLDER / "Example_with_walkway.txt"

if __name__=="__main__":
    # Loading Config File
    matrix:List[List[Optional[Seat]]]
    if not LAYOUT_FILE_NAME.exists():
        Logger.error(f"Seat Layout File does not exist: {LAYOUT_FILE_NAME}")
        Logger.debug(f"Current location is: {Path(__file__)}")
    else:
        Logger.debug("File exists, attempting to parse it.")
        try:
            matrix = Loader.load_seat_config(str(LAYOUT_FILE_NAME)) #Would like to parse Path Object 
            Logger.debug("\nPure Seat Layout Matrix")
            Logger.debug(matrix)
        except Exception:
            Logger.error("Failed to parse file")

    # Parsing into wrapper class
    standart_layout:SeatLayout = SeatLayout(matrix, "Standart Layout I")
    Logger.debug(f"\nPlane Seat Layout Class Rep:\n {standart_layout.print_seats()}")

    # Putting Seat Layout into PlaneConfig
    standart_plane:PlaneConfig = PlaneConfig([standart_layout], "Standart Plane I")
    
    Logger.debug(f"PlaneConfig Print Statement: \n{str(standart_plane)}")