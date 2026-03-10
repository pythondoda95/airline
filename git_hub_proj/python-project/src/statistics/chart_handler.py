#!usr/bin/python 

import numpy as np 
import matplotlib as mpl 
import matplotlib.pyplot as plt 
import os
from typing import Dict, List, Optional, Union, Any
import shutil #For Creating tar Archives and Checking Installed Software
import zipfile
from pathlib import Path
import traceback 

from seat_data.plane import Plane
from seat_data.price_data import PricingConfig
from util.logger import Logger

RES_DIR = Path(__file__).resolve().parent.parent.parent / "data/"

STAT_OUTPUT_PATH = RES_DIR / "stat_output"
IMG_OUTPUT_PATH = RES_DIR / "image_files"
ARCHIVE_OUTPUT_PATH = RES_DIR / "archives"

"""
Two Classes for Creating and Managing Image Charts, Archives, PDF...
Compatibility was only checked and build for Linux, not Windows!!!
By @Paul with Help from @Felix 
"""
class ChartManager():
    """ Class for creating, editing, deleting charts and related files"""
    def __init__(self):
        """ Init for ChartManager"""
        self.standart_folder = IMG_OUTPUT_PATH
        self.logger = Logger() #Add Default Logger 

        if not self.standart_folder.exists():
            self.standart_folder.mkdir(parents=True, exist_ok=True)

        # NOTE Check if typst is installed on the system (Required for PDF Creation)
        program_name = "typst"
        if shutil.which(program_name):
            self.logger.debug(f"{program_name} is installed. PDF Creator is usable")
        else:
            self.logger.warn(f"{program_name} is not installed. PDF Creator is not usable")  

    def delete_file(self, filename: str, confirm:bool = True) -> bool:
        """
        Deletes a specific file by name from the standard folder.
        Returns True if successful, False otherwise.
        """
        file_path:Path = self.standart_folder / filename
        if not file_path.is_file():
            self.logger.warn(f"File not found: {file_path}")
            return False

        try:
            if confirm:
                if not input(f"Are you sure you want to delete {file_path}? yes/no  ") == "yes":
                    self.logger.debug(f"Aborting File deletion for {file_path}")
                    return
            file_path.unlink() #NOTE unlink is the same as .remove()
            self.logger.note(f"Deleted file: {file_path}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to delete file {file_path}: {e}")
            return False

    def clear_files(self, confirm:bool = True, safe: bool = False, filetype: List[str] = (".png", ".jpg", ".jpeg")) -> int:
        """
        Deletes all files from the standard folder.
        Use safe mode to delete only specified file types.
        Returns the number of deleted files.
        """
        deleted_count = 0
        self.logger.warn(f"Deleting statistic files from {self.standart_folder}.")

        if not self.standart_folder.is_dir():
            self.logger.error(f"Folder does not exist or is not a directory: {self.standart_folder}")
            return 0
        if confirm:
            if not input(f"Are you sure you want to delete multible files? yes/no  ") == "yes":
                self.logger.debug(f"Aborting File deletions")
                return

        for file_path in self.standart_folder.iterdir():
            if file_path.is_file():
                if safe and file_path.suffix.lower() not in [ft.lower() for ft in filetype]:
                    continue  # Skip files not in allowed types
                try:
                    file_path.unlink()
                    deleted_count += 1
                except Exception as e:
                    self.logger.error(f"Failed to delete file {file_path}: {e}")
    
    def compress_folder(self, name: str = "Archive", format: str = ".zip") -> bool:
        """
        Compresses the statistics folder into an archive and moves it to the destination.
        @name: name of the archive (without extension)
        @format: compression format (".zip", ".tar.gz", etc.)
        """
        if not STAT_OUTPUT_PATH.exists():
            STAT_OUTPUT_PATH.mkdir(parents=True, exist_ok=True)

        archive_name = f"{name}{format}"
        archive_path = ARCHIVE_OUTPUT_PATH / archive_name

        try:
            # Standart .zip Archive
            # zip Compresses folder into single archive file using DEFLATE
            # https://docs.python.org/3/library/zipfile.html
            if format.lower() == ".zip":
                with zipfile.ZipFile(archive_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                    for file_path in self.standart_folder.rglob("*"):
                        if file_path.is_file():
                            arcname = file_path.relative_to(self.standart_folder)
                            zipf.write(file_path, arcname=arcname)
                self.logger.note(f"Successfully created ZIP archive: {archive_path}")

            # TAR (Tape Archive)
            # tar.gz and .tgz are the same
            # uncompressed archive file, keeping any metadata (permissions,ownership,timestamps)
            # https://docs.python.org/3/library/shutil.html#shutil.make_archive
            elif format.lower() in (".tar.gz", ".tgz"):
                with shutil.make_archive(
                    str(archive_path.with_suffix("")),  # Remove .gz from name
                    'gztar',
                    root_dir=self.standart_folder
                ) as tar_path:
                    shutil.move(tar_path, archive_path)
                self.logger.note(f"Successfully created TAR.GZ archive: {archive_path}")
            
            # Compressed Tarball Archive 
            elif format.lower() == ".tar":
                with shutil.make_archive(
                    str(archive_path.with_suffix("")),
                    'tar',
                    root_dir=self.standart_folder
                ) as tar_path:
                    shutil.move(tar_path, archive_path)
                self.logger.note(f"Successfully created TAR archive: {archive_path}")

            else:
                self.logger.error(f"Unsupported archive format: {format}. Aborting!")
                return False

            return True

        except Exception as e:
            self.logger.error(f"Failed to compress folder {self.standart_folder} to {archive_path}: {e}")
            return False
        
    def list_files(self) -> List[Path]:
        """
        Lists all files in the standard folder.
        Returns a list of Path objects.
        """
        if not self.standart_folder.is_dir():
            self.logger.error(f"Folder does not exist: {self.standart_folder}")
            return []

        files = [f for f in self.standart_folder.iterdir() if f.is_file() and f.name != ".gitkeep"]
        self.logger.note(f"Found {len(files)} files in {self.standart_folder}")
        for f in files:
            self.logger.note(f"├── {f.name}") #NOTE No clue what the symbol is called, got it from unix tree util
        return files
        
    def _display_chart(self, name: str) -> bool:
        """
        Displays a single chart image.
        @name: filename including extension (e.g., "chart.png")
        """
        file_path = self.standart_folder / Path(name)
        if not file_path.is_file():
            self.logger.error(f"Chart file not found: {file_path}")
            return False
        self.logger.debug("Only works on Unix Systems (Most likely)")
        try:
            os.system(f"xdg-open {file_path}")
            self.logger.note(f"Displayed chart: {file_path}")
            return True
        except Exception:
            return False

    
    def display_charts(self, names):
        """ 
        Displays n amount of charts 
        @names The Images to be opened 
        """ 
        for img in names:
            try:
                self._display_chart(img)
            except Exception as e:
                self.logger.error(f"Failed to open image with: {e}")
        
    def images_to_pdf(self, plane:Plane) -> int:
        """ 
        Moves all image files into a singular pdf.
        """
        filepath = STAT_OUTPUT_PATH / f"{plane.name}.typ"

        path_list = self.list_files()

        typst_image_names:List[str] = []
        if path_list:
            for path in path_list:
                typst_image_names.append(f"#image(\"../{IMG_OUTPUT_PATH.name}/{path.name}\")\n")
        try:
            with open(filepath, 'w') as f:
                f.write(f"""
                = {plane.name}
                == Plane Raw Data 
                {plane.display_full_info(display_padding=False)}
                
                == Created Statistic Charts
                {"".join(typst_image_names)}
            """)
        except Exception as e:
            self.logger.error(f"Failed to create raw Typst File with error: {e}\nTraceback: {e.__traceback__.tb_lineno}\n")
        try:
            os.system(f"typst compile {filepath} --root ./../")
        except Exception as e:
            self.logger.error(f"Failed to compile typst file to pdf. Error: {e}")
        self.logger.warn("Even it throws something that looks like an error, It might have created a working pdf file (PDF Creator)")

class ChartCreator():
    """ 
    Class for Creating Charts
    """
    # NOTE If more usage then the current (19.02.2026) is needet, rewrite the entire thing. It works but it is very frail and badly scalable
    def __init__(self):
        pass

    def plot_data(
        self,
        plot_type: str,
        data: Union[Dict[str, List], List, Dict[Any, Any]],  # Updated type hint
        x_label: Optional[str] = None,
        y_label: Optional[str] = None,
        _labels: Optional[List[str]] = None, # Horrible workarround for a stupid problem 
        title: Optional[str] = None,
        file_name: Optional[str] = None,
        display: bool = True
    ) -> None:
        """
        Generate and display and/or save a plot using matplotlib.
        
        Args:
            @plot_type: Type of supported plot. Available:'bar', 'line', 'pie'
            @data: Data for the plot
            @x_label: x-axis label (optional)
            @y_label: y-axis label (optional)
            @labels: Workaround for a stupid problem (optional)
            @title: Plot title (optional)
            @file_name The FIlename to save as
            @display: Whether to display the plot
        
        Supported data structures:
            - Bar/Line: 
                * {'x': [x_values], 'y': [y_values]} 
                * [y_values] (x defaults to 0,1,2...)
                * {x_value1: y_value1, x_value2: y_value2, ...} (keys as x, values as y)
            - Pie: [values] (labels default to 0,1,2...)
        
        Raises:
            ValueError: If plot_type is unsupported or data structure is invalid
        
        By @Paul with support from Qwen 3 30B A3B Thinking 2507
        """
        # Validate plot type
        valid_types = ['bar', 'line', 'pie']
        if plot_type.lower() not in valid_types:
            raise ValueError(f"Unsupported plot type. Valid: {valid_types}")
        
        # Create figure and axis
        fig, ax = plt.subplots()
        
        # Handle different plot types
        if plot_type.lower() == 'bar':
            if isinstance(data, list):
                # List of y values (x defaults to 0,1,2,...)
                ax.bar(range(len(data)), data)
            elif isinstance(data, dict):
                # Check for 'x' and 'y' keys first
                if 'x' in data and 'y' in data:
                    ax.bar(data['x'], data['y'])
                # Check for dictionary with keys as x and values as y
                elif all(isinstance(k, (str, int, float)) for k in data.keys()):
                    x = list(data.keys())
                    y = list(data.values())
                    ax.bar(x, y)
                else:
                    raise ValueError("Bar plot requires dict with 'x' and 'y' keys, list of values, or {x: y} dictionary")
            else:
                raise ValueError("Bar plot requires list of values or dict with 'x' and 'y' keys or {x: y} dictionary")
        
        elif plot_type.lower() == 'line':
            if isinstance(data, list):
                # List of y values (x defaults to 0,1,2,...)
                ax.plot(range(len(data)), data)
            elif isinstance(data, dict):
                # Check for 'x' and 'y' keys first
                if 'x' in data and 'y' in data:
                    ax.plot(data['x'], data['y'])
                # Check for dictionary with keys as x and values as y
                elif all(isinstance(k, (str, int, float)) for k in data.keys()):
                    x = list(data.keys())
                    y = list(data.values())
                    ax.plot(x, y)
                else:
                    raise ValueError("Line plot requires dict with 'x' and 'y' keys, list of values, or {x: y} dictionary")
            else:
                raise ValueError("Line plot requires list of values or dict with 'x' and 'y' keys or {x: y} dictionary")
        
        elif plot_type.lower() == 'pie':
            if isinstance(data, list):
                if not _labels:
                    ax.pie(data, labels=range(len(data)))
                else:
                    ax.pie(data, labels=_labels)
            else:
                raise ValueError("Pie chart requires list of values")
        
        # Set labels and title
        if x_label:
            ax.set_xlabel(x_label)
        if y_label:
            ax.set_ylabel(y_label)
        if title:
            ax.set_title(title)
        
        # Save and/or display
        if file_name:
            if not IMG_OUTPUT_PATH.exists():
                IMG_OUTPUT_PATH.mkdir(parents=True, exist_ok=True)
                print(f"Created output directory: {IMG_OUTPUT_PATH}")
            plt.savefig(IMG_OUTPUT_PATH / file_name)
            print(f"Plot saved as {file_name}")
        if display:
            plt.show()
