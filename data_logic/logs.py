import logging
from data_logic.const import COEF

# Ici, on initialise tout les logger, des objets qui nous permettent d'affichier différentes variable sans trop changer le code. 
# Permet de séléctionner des niveau de logs pour chaque logger individuellement.

def set_logger(name : str) : 
    logger = logging.getLogger(name)
    if not logger.handlers:
        # Format the logger_corres messages
        formatter = logging.Formatter('%(name)s - %(message)s')

        handler = logging.StreamHandler()
        handler.setFormatter(formatter)

        
        # Add the corres_handler as the only handler
        logger.addHandler(handler)
        
        # Set propagate to False to prevent messages from being propagated to the root logger
        logger.propagate = False
    return logger



# Set the logging level
logger_corres = set_logger("Correspondance")

logger_erreurs = logging.getLogger("erreurs")

def log_correspondance(username1, username2, correspondance):
    message = f"{username1} et {username2} : {round(correspondance* 100, 3) }%"
    if username1[:-1] == username2[:-1]:
        message = "TRUE " + message
    else : 
        message = "     " + message
        
    logger_corres.info(message)


logger_corrections = set_logger("correction")

logger_intersection = logging.getLogger("intersection")



logger_SIF = set_logger("SIF")

logging.basicConfig()



import logging
data_logger = logging.getLogger("data_logger")