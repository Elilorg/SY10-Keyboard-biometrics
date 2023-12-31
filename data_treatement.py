from data_logic.file_manip import load_json
from data_logic import creer_fichier_lettre
from data_logic import user_data_from_lettres
from data_logic import evaluate_correspondance
from data_logic.const import CHEMIN_DOSSIER_SESSION, CHEMIN_DOSSIER_LETTRES 
from data_logic.logs import logger_corres, logger_SIF, logger_corrections
from data_logic.logs import data_logger 
import logging
import time

## Ce fichier contient les appels des fonctions a data_logic. C'est l'interface entre les maths et le site web. 

data_logger.setLevel(logging.DEBUG)

logger_corres.setLevel(logging.DEBUG)
logger_SIF.setLevel(logging.DEBUG)
logger_corrections.setLevel(logging.ERROR)

import json

def clear_keys(name):
    """
    Vide keys.json et traite son contenu.
    paramètres:
        name: nom à donner au fichier
    """
    data_logger.info("CLEAR KEYS")
    key_file_name = save_key_file()
    data_logger.info("KEY_FILE : " , key_file_name)
    if key_file_name is not None :
        data_logger.info("KEY_FILE is not empty")
        save_keys_to_user_data(key_file_name)
    else : 
        data_logger.info("KEY_FILE is empty")
    # Create new keys.json containing '[]'
    with open('keys.json', 'w') as json_file:
        json.dump([], json_file)

def identify_user():
    name = save_key_file() # Name est toujours IDENTIFYs
    save_keys_to_user_data(name)
    users = get_user_list()
    correspondances=[]
    for user in users:
        corres = evaluate_correspondance(user, "IDENTIFY")
        entry = [user, round(corres*100, 2)]
        correspondances.append(entry)
    # trie les correspondances en fonction de leurs valeurs
    correspondances = sorted(correspondances, key=lambda x: x[1], reverse=True)
    for i in correspondances:
        i[1] = str(i[1])
    #score = correspondances2[sorted_keys[0]] - correspondances2[sorted_keys[1]]
    # message = sorted_keys[0]+" | "+str(round(score*100, 2))
    #print(correspondances)
    return correspondances


def log_correspondances(correspondances2 : dict):
    sorted_keys = sorted(correspondances2.keys(), key=lambda k: correspondances2[k], reverse=True)
    data_logger.info("DETECTED USER : " + sorted_keys[0] + f" : {correspondances2[sorted_keys[0]]}")
    for key in sorted_keys[1:]:
        data_logger.info(f"      {key} : {round(correspondances2[key], 2)}")

def save_key_file() : 
    """
    copie le dictionnaire de session dans un fichier
    Pour le dictionnaire de IDENTIFY, ca écrasera le fichier keys a chaque fois. 
    """
    data_logger.info("SAVE KEYS")
    with open('keys.json', 'r') as json_file:
        donnees = json.load(json_file)
    if len(donnees) == 0:
        return None
    donnees = donnees[0]
    nom = donnees["name"]
    
    with open(f"{CHEMIN_DOSSIER_SESSION}/{nom}.json", "w") as json_file:
        json.dump([donnees],  json_file)
    return nom


def save_keys_to_user_data(name) :
    file_name = f"{CHEMIN_DOSSIER_SESSION}/{name}.json"
    donnees = load_json(file_name)
    if len(donnees) == 0:
        time.sleep(0.1)
        if len(donnees) == 0:
            return
        else : 
            donnees = load_json(file_name)
    donnees = donnees[0]
    nom = donnees.get("name", "DEFAULT")
    data_logger.info("CREATE FICHIER LETTRE")
    creer_fichier_lettre(donnees, nom)
    data_logger.info("CREATE FICHIER USER")
    user_data_from_lettres(nom, load_json(CHEMIN_DOSSIER_LETTRES+nom+".json"))


def get_user_list():
    """
    renvoie la liste des noms des utilisateurs enregistrés dans users.json
    """
    users = load_json("users.json")
    return [user for user in users.keys() if user != "IDENTIFY"]

if __name__ == "__main__":
    clear_keys("NAME")