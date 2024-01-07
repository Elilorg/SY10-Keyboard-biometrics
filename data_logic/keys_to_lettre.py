import json
import os
from data_logic.const import TREATED_FILE_PATH , SESSION_FILE_PATH
from data_logic.file_manip import load_json

### NE SERT QU'A GENERER LES FICHIERS LETTRE. UTILISÉ UNE FOIS

def unifier_liste(data : list[dict]):
    """
    Prend la liste de data (listes qui représentent des mots) et renvoie une seule liste qui contient tous les évenements
    paramètre :
        - data : list[list[dict]]
    renvoie :
        - liste_unifiee : list[dict]
    """
    liste_unifiee = []
    for word in data:
        liste_unifiee += word
    return liste_unifiee

def group_by_lettre(data : list[dict]):
    """
    Prend la donnée des fichiers de session et regroupe les évenement press et release par lettre 
    Ainsi, chaque lettre ecrite est dans un dictionnaire qui rescence toutes les informations qui lui sont propre
    paramètres :
        data (list[list[dict]]) : la donnée des fichiers de session
    renvoie :
        lettres (list[dict]) : la liste des lettres ou chaque dict est une lettre
    """
    lettres = []
    for index, keyevent in enumerate(data) : 
        if keyevent["pressed"] == 0:
            #find release
            release = None
            for event in data[index:]:
                if event["pressed"] == 1 and event["char"].upper() == keyevent["char"].upper(): # upper pour pas considérer difféemment E et e 
                    release = event
                    break
            
            if release == None:
                print(f"{keyevent['char']} at timestamp {keyevent['timestamp']} never released")
            else:
                press_release_time = release["timestamp"] - keyevent["timestamp"]

                lettre = {
                    "keycode": keyevent["keycode"],
                    "char": keyevent["char"],
                    "time_pressed": keyevent["timestamp"],
                    "time_released": release["timestamp"],
                    "hold_time": press_release_time,
                }    
                lettres.append(lettre)
    # Ajout des press press time au lettres
    precedent = None
    lettres[0]["press_press_time"] = -1
    for lettre in lettres:
        if precedent:
            press_press_time = lettre["time_pressed"] - precedent["time_pressed"]
            lettre["press_press_time"] = press_press_time

        precedent = lettre

    return lettres

def pretraitement(donnees): # les donnees sont un dictionnaire de session venant des fichier keys
    """
    Rassemble les touches en une seule liste et par lettre.
    donnees : dict{data : list[list[dict]]}
    """
    
    data = donnees["data"]
    data = unifier_liste(data)
    lettres = group_by_lettre(data)
    return lettres

def write_lettres(lettres, filename, append = True):
    """
    Ecrit les lettres dans un fichier au nom de l'utilisateur
    """
    ## overwrite si user is indentify et si append = False
    ## sinon ajoute au fichier
    lettres_user = []
    if (filename != "IDENTIFY.json" and os.path.exists(TREATED_FILE_PATH + filename)) and append == True:
        lettres_user = load_json(TREATED_FILE_PATH + filename)
    lettres_user += lettres

    with open(TREATED_FILE_PATH + filename, 'w') as f:
        json.dump(lettres_user, f, indent=4)

def creer_fichier_lettre(donnees, name : str = None):
    """
    donnees : un dictionnaire de session (1 seule session)
    """
    lettres = pretraitement(donnees)
    if name == None:
        name = donnees["name"]
    write_lettres(lettres, filename=f"{name}.json")

def from_session_to_lettre(filename, tous = False, name = None):
    """
    Transforme les fichiers de session en fichiers lettre
    - filename (str) : le nom du fichier json de session
    - name (str) : le nom de la personne. si non renseigné, on prend le premier
    - tous (bool) : si true, on traite toute les session du fichier, quel que soit la variable name
    """
    if tous :
        for session in load_json(SESSION_FILE_PATH + filename):
            creer_fichier_lettre(session)
    elif name == None : 
        session = load_json(SESSION_FILE_PATH + filename)[0]
        creer_fichier_lettre(session)
    else : 
        sessions = load_json(SESSION_FILE_PATH + filename, name=name)
        session = list(filter(lambda x : x["name"] == name, sessions))[0]
        creer_fichier_lettre(session, name=name)