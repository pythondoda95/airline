import tkinter as tk
import sys

from cli import CLI
from login.main import SystemApp
from seat_data.plane import Plane, PlaneInitError
from util.logger import Logger
from util.system_tool import SysTools
from statistics.chart_handler import ChartManager 
from statistics.creation_calls import PlaneChartCreations

HELP_MESSAGE = """
Usage:
    (A) python3 main.py -h
    (B) python3 main.py SEAT_LAYOUT_FILE

Explanation:
    Executing (A) displays this help message.

    Executing (B) starts the default program. The argument SEAT_LAYOUT_FILE is 
    the name of one of the files in data/seat_configs (without extension,
    e.g. "economy") describing that plane's seat layout.
"""


# App state
plane = None
username = None
uid = None  # user ID
is_admin = False

# Logger & Util Tools 
logger = Logger()
util = SysTools()

def main():
    exit_message = parse_arguments()
    if exit_message is not None:
        logger.error(exit_message)
        return

    cli = (CLI().static_prompt("Welcome to the BingBong Airlines Management System.")
                .no_back()
                .add("Login / sign up", run_login))
    cli.run()


def parse_arguments():
    """Parses the command line arguments and initializes the app state via global
    variables. If everything works, return None, if something goes wrong, return
    a message describing the problem.
    """

    n_args = len(sys.argv) - 1  # First element is the script's name, we ignore that.

    if n_args == 0:
        return "Error: Invalid arguments. Use -h for help."

    if n_args == 1:
        if sys.argv[1] == "-h":
            return HELP_MESSAGE

        seat_layout_file = sys.argv[1]

        global plane
        try:
            plane = Plane(seat_layout_file)
        except PlaneInitError as e:
            return f"Error: {e.message}"

        return

    if n_args > 1:
        return f"Error: Expected one argument but got {n_args}. Use -h for help.\n Args: {sys.argv}"


def run_login():
    global username, uid, is_admin

    root = tk.Tk()
    app = SystemApp(root, skip_dashboard=True)
    root.mainloop()

    if app.current_user is None:
        username = None
        uid = None
        is_admin = False
        return
    else:
        username = app.current_user[1]
        uid = app.current_user[0]
        is_admin = app.is_admin
        
    if is_admin:
        show_admin_menu()
    else:
        show_normal_user_menu()


def show_normal_user_menu():
    global username, plane

    get_prompt = lambda: f"You are logged in as {username}. What do you want to do?"

    (CLI().dynamic_prompt(get_prompt)
          .add("Display seats", lambda: print(plane.render_as_text(True)))
          .add("See my reservations", lambda: print("\n".join(plane.get_user_reservations(uid))))
          .add("Make a reservation", make_reservation) 
          .add("Cancel a reservation", cancel_reservation)
          .run())


def make_reservation():
    global uid

    seat_coords = CLI.input("Please enter the seat for which you want to make a reservation. (Format: 'Row:Column', 0-based): ")

    try:
        plane.make_reservation(seat_coords, uid)
        print(f"Successfully reserved seat {seat_coords} for you.")
    except ValueError:
        print(f"Error: '{seat_coords}' is not a seat that you can make a resertvation for.")


def cancel_reservation():
    global uid, is_admin

    seat_coords = CLI.input("Please enter the seat for which you want to cancel your reservation. (Format: 'Row:Column', 0-based): ")

    if not is_admin and seat_coords not in plane.get_user_reservations(uid):
        print(f"Error: You have no reservation for seat {seat_coords}.")
        return

    try:
        plane.cancel_reservation(seat_coords)
        print(f"Successfully cancelled your reservation for seat {seat_coords}.")
    except ValueError:
        print(f"Error: '{seat_coords}' is not a seat that currently has a reservation.")


def show_admin_menu():
    chart_manager = ChartManager()
    (CLI().static_prompt("You are logged in as an admin. What do you want to do?")
        .add("Display seats", lambda: print(plane.render_as_text()))
        .add("Display statistics summary", lambda: print(plane.display_full_info()))
        .add("Cancel a reservation", cancel_reservation)
        .add("Enter Advanced admin options", show_admin_advanced_menu)
        .run())

def show_admin_advanced_menu():
    chart_manager = ChartManager()
    pcc = PlaneChartCreations(plane)
    (CLI().static_prompt("You are logged in as an admin and in the advanced options menu. What do you want to do?")
        .add("Clear Terminal", lambda: util.clear_terminal())
        .add("List Files", lambda: chart_manager.list_files())
        .add("Display Chart(s)", lambda: chart_manager.display_charts(list(input("Write a comma seperated list of files you wish to display. ").split(","))))
        .add("Create and View All Available Charts", lambda: pcc.create_all_charts()) 
        .add("Delete File(s)", lambda: chart_manager.delete_file(input("What is the full name of the file to delete? ")))
        .add("Create PDF from all created data", lambda: chart_manager.images_to_pdf(plane))
        .add("Compress Folder", lambda: chart_manager.compress_folder(name=input("What should the archive be named? ").strip(), format=input("Desired archive format? ").strip()))
        .run())


if __name__=="__main__":
    main()