import logging


# This creates a logger object named logger
logger = logging.getLogger(__name__)

# This means that we are setting up the level above or equal to what 
# severity we want to display the log for
logger.setLevel(logging.INFO)

# Time--name that is logger here--INFO/ERROR/..--message
formatter = logging.Formatter('%(asctime)s %(name)s %(levelname)s %(message)s')


# The below three lines are used to display the output of the logger on to the console
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)

# The below three lines are used to display the output on to the logger on to the file "app.log"
file_handler = logging.FileHandler('app.log')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)