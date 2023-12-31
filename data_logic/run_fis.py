import subprocess
from data_logic.logs import logger_SIF
import logging
logger_SIF.setLevel(logging.DEBUG)

def run_fis(*args):
    """
    Renvoie le résultat de l'execution du fichier algo_complet.m avec les arguments passés en paramètre.
    Paramètres de la fonction :
        - pourcentage de substitutions [0;1] (cappé à 1)
        - ratio d'erreurs [0;1]
        - rollover ratio [0;1]
        - vitesse de frape [0;200]
        - possiblité de mauvais dans 2eme variable SF2
        - possiblité de moyen dans 2eme variable SF2
        - possiblité de bon dans 2eme variable SF2
    """
    values = [str(x) for x in args]
    output = subprocess.check_output(['octave-cli', './data_logic/octave/algo_complet.m']+values)
    text_output = output.decode("utf-8")
    logger_SIF.info(text_output)
    #return text_output
    ligne = text_output.split('\n')[2]
    result_sif3 = ligne.split("=")[1].replace("{", "").replace("}", "").replace("(", "").replace(")", "")
    result_sif3 = result_sif3.split(",")
    mauvais, bon = list(map(lambda x : float(x.split(";")[1]), result_sif3))

    return bon, mauvais
    

if __name__ == '__main__':
    out = run_fis(0.02, 0.06, 0.2, 181, 1, 1, 1)
    # converti depuis byte en string
    print(out)
