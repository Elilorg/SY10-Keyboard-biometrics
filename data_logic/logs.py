import logging
import datetime
from data_logic.const import COEF
# Create a logger
logger_corres = logging.getLogger("Correspondance")

# Set the logging level
logger_corres.setLevel(logging.INFO)

# Check if the logger has any handlers
if not logger_corres.handlers:
    # Format the logger_corres messages
    formatter = logging.Formatter('%(name)s - %(message)s')

    corres_handler = logging.StreamHandler()
    corres_handler.setFormatter(formatter)


    corres_file = f'./logs/correspondance_coef{COEF}.log'
    log_file_corres_handler = logging.FileHandler(corres_file)
    
    # Add the corres_handler as the only handler
    logger_corres.addHandler(corres_handler)
    logger_corres.addHandler(log_file_corres_handler)
    
    # Set propagate to False to prevent messages from being propagated to the root logger
    logger_corres.propagate = False

print(logger_corres.handlers[0])


logger_erreurs = logging.getLogger("erreurs")

def log_correspondance(username1, username2, correspondance):
    message = f"{username1} et {username2} : {round(correspondance* 100, 3) }%"
    if username1[:-1] == username2[:-1] :
        message = "TRUE " + message
    else : 
        message = "     " + message
        
    logger_corres.info(message)


logger_intersection = logging.getLogger("intersection")
logging.basicConfig()
