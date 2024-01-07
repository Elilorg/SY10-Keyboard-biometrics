from data_logic.file_manip import load_json
from data_logic import creer_fichier_lettre
from data_logic import user_data_from_lettres
from data_logic import evaluate_correspondance
from data_logic.const import SESSION_FILE_PATH, TREATED_FILE_PATH
from data_logic.logs import logger_corres
from loggers import data_logger 
import logging

data_logger.setLevel(logging.ERROR)

logger_corres.setLevel(logging.DEBUG)

import json

def clear_keys(name):
    """
    Vide keys.json et traite son contenu.
    paramètres:
        name: nom à donner au fichier
    """
    save_key_file()
    save_keys_to_user_data()
    # Create new keys.json containing '[]'
    with open('keys.json', 'w') as json_file:
        json.dump([], json_file)

def identify_user():
    save_keys_to_user_data()
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
    print(correspondances)
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
    with open('keys.json', 'r') as json_file:
        donnees = json.load(json_file)
    if len(donnees) == 0:
        return
    donnees = donnees[0]
    nom = donnees["name"]
    
    with open(f"{SESSION_FILE_PATH}/{nom}.json", "w") as json_file:
        json.dump([donnees],  json_file)


def save_keys_to_user_data():
    donnees = load_json("keys.json")
    if len(donnees) == 0:
        return
    donnees = donnees[0]
    nom = donnees.get("name", "DEFAULT")
    creer_fichier_lettre(donnees, nom)
    user_data_from_lettres(nom, load_json(TREATED_FILE_PATH+nom+".json"))


def get_user_list():
    """
    renvoie la liste des noms des utilisateurs enregistrés dans users.json
    """
    users = load_json("users.json")
    return [user for user in users.keys() if user != "IDENTIFY"]

if __name__ == "__main__":
    clear_keys("NAME")