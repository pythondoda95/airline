# file_handling/reservation_database.py
import sqlite3
from pathlib import Path
from datetime import datetime


class ReservationDatabase:
    """
    Very simple database helper for reservations.
    Uses SQLite file: src/login/system.db
    """

    def __init__(self, db_path=None):
        if db_path is None:
            src_dir = Path(__file__).resolve().parent.parent  # .../src
            db_path = src_dir / "login" / "system.db"

        self.db_path = Path(db_path)
        self._create_table()

    def _connect(self):
        return sqlite3.connect(self.db_path)

    def _create_table(self):
        self.db_path.parent.mkdir(parents=True, exist_ok=True)

        con = self._connect()
        cur = con.cursor()

        cur.execute("""
    CREATE TABLE IF NOT EXISTS reservations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        userID INTEGER NOT NULL,
        layout_name TEXT NOT NULL,
        seat TEXT NOT NULL,
        reserved_at TEXT NOT NULL,
        UNIQUE(layout_name, seat)
    )
""")
        con.commit()
        con.close()

    def reserve_seat(self, user_id, layout_name, seat):
        """
        Try to reserve one seat.
        Returns True if success, False if seat is already taken.
        """
        con = self._connect()
        cur = con.cursor()

        time_now = datetime.now().isoformat(timespec="seconds")

        try:
            cur.execute(
                "INSERT INTO reservations (userID, layout_name, seat, reserved_at) VALUES (?,?,?,?)",
                (user_id, layout_name, seat, time_now),
            )
            con.commit()
            con.close()
            return True
        except sqlite3.IntegrityError:
            con.close()
            return False

    def cancel_own_seat(self, user_id, layout_name, seat):
        """
        User cancels own reservation.
        Returns True if removed, False if not found.
        """
        con = self._connect()
        cur = con.cursor()

        cur.execute(
            "DELETE FROM reservations WHERE userID=? AND layout_name=? AND seat=?",
            (user_id, layout_name, seat),
        )
        con.commit()

        deleted = cur.rowcount > 0
        con.close()
        return deleted

    def cancel_any_seat(self, layout_name, seat):
        """
        Admin cancels any reservation for this seat.
        Returns True if removed, False if not found.
        """
        con = self._connect()
        cur = con.cursor()

        cur.execute(
            "DELETE FROM reservations WHERE layout_name=? AND seat=?",
            (layout_name, seat),
        )
        con.commit()

        deleted = cur.rowcount > 0
        con.close()
        return deleted

    def seat_is_taken(self, layout_name, seat):
        """
        Returns True if seat is reserved.
        """
        con = self._connect()
        cur = con.cursor()

        cur.execute(
            "SELECT 1 FROM reservations WHERE layout_name=? AND seat=?",
            (layout_name, seat),
        )
        row = cur.fetchone()
        con.close()

        return row is not None

    def get_all_reservations(self):
        """
        Returns a list of tuples: (user_id, layout_name, seat, reserved_at)
        """
        con = self._connect()
        cur = con.cursor()

        cur.execute("SELECT userID, layout_name, seat, reserved_at FROM reservations")
        rows = cur.fetchall()

        con.close()
        return rows

    def get_reservation(self, userID:str):
        """
        Returns the reservations attached to the user. (Non if not existant)
        """
        con = self._connect()
        cur = con.cursor()

        cur.execute(f"SELECT userID, layout_name, seat, reserved_at FROM reservations WHERE userID = ?", (userID,))
        rows = cur.fetchall()

        con.close()
        return rows
    
    def get_reservation_for_plane(self, userID:str, plane:str):
        """
        Returns the reservations attached to the user for a specific plane (Non if not existant)
        """
        con = self._connect()
        cur = con.cursor()

        cur.execute(f"SELECT userID, layout_name, seat, reserved_at FROM reservations WHERE userID = ? AND layout_name = ?", (userID, plane))
        rows = cur.fetchall()

        con.close()
        return rows
