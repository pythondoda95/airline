#!/usr/bin/env python3

# Based on APP SS 2024/25 Logger & Arthur Admin Logger
# Traceback Functionality is Written by some Qwen AI Modle 

import traceback
import sys
from typing import Optional
from datetime import datetime
from pathlib import Path

LOG_DIR = Path(__file__).resolve().parent  # Path where to save the logfiles to

class Color:
    """ANSI Escape Sequences for colors in terminal"""
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class Logger:
    """
    Functions for logging.
    If the terminal does not support colors, enable display_text.
    Traceback functionality does work but is not usefull - Only use if you know what you are doing 
    By @Paul
    """
    LOG_LEVEL_OVERWRITE: Optional[int] = None  # Class variable, used for centrall override 

    def __init__(self, max_level: int = 5, logfile: Optional[str] = None, display_text: bool = False, overwrite: Optional[int] = None):
        self.max_level = max_level
        self.display_text = display_text
        self.logfile = (LOG_DIR / Path(logfile)) if logfile else None

        if overwrite: self.max_level = overwrite # Overwrite class variabel. Use with Caution
        if self.logfile: self.logfile.parent.mkdir(parents=True, exist_ok=True) # Create Log File folder if not exists

    def debug(self, text: str) -> None:
        if self.max_level < 1: return
        message = f"Debug: {text}" if self.display_text else text
        print(f"{Color.OKCYAN}{message}{Color.ENDC}")
        if self.logfile:
            self._write_to_file(message)
        
    def note(self, text: str) -> None:
        if self.max_level < 2: return
        message = f"Note: {text}" if self.display_text else text
        print(f"{Color.OKGREEN}{message}{Color.ENDC}")
        if self.logfile:
            self._write_to_file(message)

    def warn(self, text: str) -> None:
        if self.max_level < 3: return
        message = f"Warning: {text}" if self.display_text else text
        print(f"{Color.WARNING}{message}{Color.ENDC}")
        if self.logfile:
            self._write_to_file(message)

    def error(self, text: str, exception: Optional[Exception] = None) -> None:
        """Log an error message, optionally with an exception to show the line number.
        
        Args:
            text: The error message to log
            exception: Optional exception to include with line number information
        """
        # NOTE The traceback functioanlity is kinda shit since it returns the last trace step, wich is often some external library
        if self.max_level < 4: return
        
        # Handle Exception 
        if exception:
            # Get the traceback information
            tb = traceback.extract_tb(sys.exc_info()[2])
            # Get the last frame (the one that caused the exception)
            frame = tb[-1]
            filename = frame.filename
            line_number = frame.lineno
            function_name = frame.name
            
            # Format the error message
            error_message = f"Exception: {str(exception)}"
            if text:
                error_message += f" - {text}"
            
            # Format the line information
            line_info = f" (File: {filename}, Line: {line_number}, Function: {function_name})"
            
            message = f"Error: {error_message}{line_info}"
        else:
            message = f"Error: {text}" if self.display_text else text
        
        print(f"{Color.FAIL}{message}{Color.ENDC}")
        if self.logfile:
            self._write_to_file(message)

    def _write_to_file(self, text: str, newline: bool = True) -> None:
        """Append a timestamped message to the logfile."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        message = f"{timestamp} | {text}"
        if newline: message += "\n"

        with self.logfile.open("a", encoding="utf-8") as f:
            f.write(message)

if __name__ == '__main__':
    l = Logger(max_level=5, logfile="test.txt", display_text=True)

    l.note("Hello, Am I Green?")
    l.debug("Hello, Am I Cyan?")
    l.warn("Hello, Am I Yellow?")
    l.error("Hello, Am I Red?")