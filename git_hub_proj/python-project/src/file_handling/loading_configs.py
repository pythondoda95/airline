from typing import List, Optional
from pathlib import Path
from copy import deepcopy

from seat_data.seat import Seat, EconomySeat, BusinessSeat, FirstClassSeat
from util.logger import Logger 
# Directory where all seat layout text files are stored
CONFIG_DIR = Path(__file__).resolve().parent.parent.parent / "data/seat_configs"


def load_seat_config(filename: str) -> List[List[Optional[Seat]]]:
    logger = Logger() # Default Logger
    """
    Load seat configuration from a text file and return a matrix.

    Returns:
        A 2D list (matrix) of Seat objects or None.
        - Seat object  -> real seat
        - None         -> aisle / walkway

    The layout file may contain:
        - A HEADER row (column labels)
        - Row numbers (1, 2, 3, ...)
        - Seat letters (A, B, C, ...)
        - '|' symbols representing walkways
    """

    full_path = CONFIG_DIR / filename

    # If the file does not exist, stop immediately
    if not full_path.is_file():
        raise FileNotFoundError(f"Seat config file not found: {filename}")
    else:
        logger.debug(f"Starting to parse {full_path}")

    matrix: List[List[Optional[Seat]]] = []
    expected_len: Optional[int] = None  # Used to ensure consistent row length

    with open(full_path, "r") as f:
        for line in f:
            line = line.strip()

            # Skip empty lines
            if not line:
                continue

            tokens = line.split()

            # --- IMPORTANT FIX ---
            # Skip header line like:
            # "HEADER A B C | D E F"
            # The header is only informational and not part of the seat matrix.
            if tokens and tokens[0].upper() == "HEADER":
                continue

            # If a row number exists (e.g. "1 A B C | D E F"),
            # remove the first token because it is not a seat.
            if tokens and tokens[0].isdigit():
                tokens = tokens[1:]

            row: List[Optional[Seat]] = []

            for t in tokens:
                if t == "|" or t== "||": 
                    # Walkway / aisle position
                    row.append(None)

                elif t == "X":
                    # Already occupied seat placeholder
                    # (Used if layout file contains visual occupancy)
                    row.append(Seat(name="occupied", char_rep="X"))

                elif len(t) == 1 and t.isalpha():
                   # --- Modified by Irem ---
                    # Map seat config tokens to new seat classes (E/B/F and legacy S)

                    tt = t.upper()

                    # Seat TYPES (new seat data)
                    if tt in ("S", "E"):  # legacy S treated as economy
                        row.append(EconomySeat(char_rep=tt))
                    elif tt == "B":
                         row.append(BusinessSeat(char_rep=tt))
                    elif tt == "F":
                         row.append(FirstClassSeat(char_rep=tt))

                       # Seat LETTERS (A, C, D, ...) for positions/labels etc.
                    else:
                          row.append(Seat(name=tt, char_rep=tt))    
                          

                else:
                    # If any unknown token appears,
                    # fail early to avoid corrupted layouts.
                    raise ValueError(f"Invalid token in seat config file: {t}")

            # Validate that all rows have equal length
            # This ensures the layout forms a proper rectangular matrix.
            if expected_len is None:
                expected_len = len(row)
            elif len(row) != expected_len:
                raise ValueError(
                    f"Inconsistent row length: expected {expected_len}, got {len(row)}"
                )
            matrix.append(row)
            
        try:
            matrix = _add_seat_position_value(matrix)
        except Exception as e:
            logger.error("Failed to add position data to seats")
        logger.debug(matrix)
        return matrix


def _add_seat_position_value(untagged:List[List[Optional[Seat]]]) -> List[List[Optional[Seat]]]:
    """ Attempt to add position value to Seat for easy value read later on"""
    untagged_copy = deepcopy(untagged)
    for i, row in enumerate(untagged_copy):
        for j, seat in enumerate(row):
            if seat is not None:  # Only assign position to seats
                seat.position = (i, j)
    return untagged_copy
