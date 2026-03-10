#!usr/bin/python

import os
import sys
from datetime import datetime

#from util.logger import Logger

"""
Collection of functions for getting info about the system that the user has and other tools regarding the system.
(Terminal Width, Language, Displayable Character, Clearing Screen...)
By @Paul
"""


class SysTools:
    @staticmethod
    def get_terminal_width() -> int:
        """Gets the max width of the terminal"""
        try:
            size = os.get_terminal_size()
            return size.columns
        except Exception as e:
            #Logger.error(e)
            return 0
        # end try

    @staticmethod
    def clear_terminal() -> None:
        """Clears all of the current terminal output (Runs the standart shell command for clearing)"""
        try:
            if sys.platform in ("linux", "darwin"):
                os.system("clear")
            elif sys.platform == "win32":
                os.system("cls")
        except Exception as e:
            raise e
        # end try

    @staticmethod
    def get_time() -> str:
        """Returns the current time without any formatting"""
        return datetime.now()

if __name__ == "__main__":
    sys_tool = SysTools()
    print(f"Terminal width: {sys_tool.get_terminal_width()}")
    print(f"Current time: {sys_tool.get_time()}")
    print(f"Current time, formatted: {sys_tool.get_time():%A, %B, %d}")
    if input("Clear Terminal: yes ?").lower() == "yes":
        sys_tool.clear_terminal()
# end main