#!usr/bin/python 

from statistics.chart_handler import ChartManager, ChartCreator
from util.logger import Logger 

if __name__=="__main__":
    # Creating ChartManager & ChartCreator Objects
    cm = ChartManager()
    cc = ChartCreator()
    logger = Logger()

    # Example data
    bar_data = {'x': ['A', 'B', 'C', 'D'], 'y': [10, 25, 15, 30]}
    line_data = [5, 15, 25, 35, 45]
    pie_data = [30, 25, 20, 15, 10]
    try:
        # Generate plots
        cc.plot_data(
            plot_type='bar',
            data=bar_data, 
            x_label='Categories', 
            y_label='Values', 
            title='Bar Chart Example', 
            file_name="bar_test", 
            display=True)
        #cc.plot_data('line', line_data, 'Index', 'Value', 'Line Chart Example', display=False, file_name='line_plot.png')
        #cc.plot_data('pie', pie_data, title='Pie Chart Example', file_name='pie_chart.png')
    except Exception as e:
        Logger.error(f"Test Chart Creation failed. Error: {e}")
    logger.debug("\n")

    try:
        # List Available Files 
        print(f"All files in the standard folder:\n {cm.list_files()}")  
    except Exception as e:
        Logger.error(f"Failed to list files. Error: {e}")
    logger.debug("\n")

    try:
        # Displaying (a) Chart(s)
        cm.display_chart("Image_Error.webp")
        cm.display_charts("Image_Error.webp", "Image_Error.webp")
    except Exception as e:
        Logger.error(f"Failed to display charts. Error: {e}")
    logger.debug("\n")
    
    try:
        # Compressing folder to zip archive 
        print(f"Compressed Folder successfully: {cm.compress_folder("archives")}")
    except Exception as e:
        Logger.error(f"Failed to compress folder. Error: {e}")
    logger.debug("\n")

    try:
        # Clear/Delete (all) Files 
        print(f"Deleted File successfully: {cm.delete_file("test.txt")}")
        print(f"File Amount: {cm.clear_files()}")
    except Exception as e:
        Logger.error(f"Failed to delete files. Error: {e}")
    logger.debug("\n")

    try:
        # Converting all data/images to a single pdf 
        cm.image_to_pdf("Combined")
        logger.debug("\n")
    except Exception as e:
        Logger.error(f"Failed to convert Files to PDF. Error {e}")    