# file_handling/reservation_service.py

from file_handling.reservation_database import ReservationDatabase
from file_handling.logs.file_logger import log_action
from file_handling.loading_configs import load_seat_config


class ReservationService:
    def __init__(self):
        self.db = ReservationDatabase()

    def _seat_ok(self, seat):
        seat = seat.strip()
        if len(seat) < 2:
            return None

        number = seat[:-1]
        letter = seat[-1]

        if not number.isdigit():
            return None
        if not letter.isalpha():
            return None

        return number + letter.upper()

    def _seat_exists_in_layout(self, layout_name, seat):
        """
        True = seat exists in the layout file.
        False = layout missing OR seat not in layout OR seat is walkway.
        """
        try:
            matrix = load_seat_config(layout_name)
        except:
            return False

        seat = self._seat_ok(seat)
        if seat is None:
            return False

        row_number = int(seat[:-1])
        seat_letter = seat[-1]

        # rows start at 1
        if row_number < 1 or row_number > len(matrix):
            return False

        row = matrix[row_number - 1]

        for cell in row:
            if cell is None:
                continue
            if cell.char_rep.upper() == seat_letter:
                return True

        return False

    def reserve(self, user_id, username, layout_name, seat):
        seat = self._seat_ok(seat)
        if seat is None:
            print("Seat format is wrong. Example: 4A")
            log_action(f"RESERVE_FAILED {username} wrong_format {layout_name} {seat}")
            return False

        if not self._seat_exists_in_layout(layout_name, seat):
            print("Seat does not exist in this layout.")
            log_action(f"RESERVE_FAILED {username} invalid_seat {layout_name} {seat}")
            return False

        ok = self.db.reserve_seat(user_id, layout_name, seat)

        if ok:
            print("Reserved!")
            log_action(f"RESERVE {username} {layout_name} {seat}")
        else:
            print("Seat is already taken.")
            log_action(f"RESERVE_FAILED {username} taken {layout_name} {seat}")

        return ok

    def cancel_own(self, user_id, username, layout_name, seat):
        seat = self._seat_ok(seat)
        if seat is None:
            print("Seat format is wrong. Example: 4A")
            log_action(f"CANCEL_FAILED {username} wrong_format {layout_name} {seat}")
            return False

        if not self._seat_exists_in_layout(layout_name, seat):
            print("Seat does not exist in this layout.")
            log_action(f"CANCEL_FAILED {username} invalid_seat {layout_name} {seat}")
            return False

        ok = self.db.cancel_own_seat(user_id, layout_name, seat)

        if ok:
            print("Cancelled!")
            log_action(f"CANCEL {username} {layout_name} {seat}")
        else:
            print("Reservation not found.")
            log_action(f"CANCEL_FAILED {username} not_found {layout_name} {seat}")

        return ok

    def admin_cancel(self, user_id, username, is_admin, layout_name, seat):
        if not is_admin:
            print("Only admin can do this.")
            log_action(f"ADMIN_CANCEL_DENIED {username} {layout_name} {seat}")
            return False

        seat = self._seat_ok(seat)
        if seat is None:
            print("Seat format is wrong. Example: 4A")
            log_action(f"ADMIN_CANCEL_FAILED {username} wrong_format {layout_name} {seat}")
            return False

        if not self._seat_exists_in_layout(layout_name, seat):
            print("Seat does not exist in this layout.")
            log_action(f"ADMIN_CANCEL_FAILED {username} invalid_seat {layout_name} {seat}")
            return False

        ok = self.db.cancel_any_seat(layout_name, seat)

        if ok:
            print("Admin cancelled!")
            log_action(f"ADMIN_CANCEL {username} {layout_name} {seat}")
        else:
            print("Reservation not found.")
            log_action(f"ADMIN_CANCEL_FAILED {username} not_found {layout_name} {seat}")

        return ok