import json
import os
from data_logic.const import CHEMIN_DOSSIER_SESSION , CHEMIN_DOSSIER_LETTRES
from data_logic.const import OMISSION, INSERTION, SUBSTITUTION
from data_logic.file_manip import load_json
from data_logic.find_error_by_text import trouver_les_différences
from data_logic.inter_space_errors import detecter_toute_les_corrections

### NE SERT QU'A GENERER LES FICHIERS LETTRE. UTILISÉ UNE FOIS



def unifier_liste(data : list[dict]):
    """
    Prend la liste de data (listes qui représentent des mots) et renvoie une seule liste qui contient tous les évenements
    paramètre :
        - data : list[list[dict]]
    renvoie :
        - liste_unifiee : list[dict]
    """
    texte_pour_chaque_mot = []
    liste_unifiee = []
    for word in data:
        texte_pour_chaque_mot.append(word[-1]["text"])
        liste_unifiee += word
    return liste_unifiee, texte_pour_chaque_mot

## FIN DU CHANTIER

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
                    "caret_pos": keyevent["caret_pos"],
                } 
                if keyevent["char"] == " ":
                    lettre["text_length"] = keyevent["text_length"]
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

def add_corrections(lettres, texte_pour_chaque_mot):
    error_count = {
        INSERTION: 0,
        OMISSION: 0,
        SUBSTITUTION: 0,
    }
    for index, texte in enumerate(texte_pour_chaque_mot[:-1]):
        mots_modifes = trouver_les_différences(texte, texte_pour_chaque_mot[index+1])
        
    
    inter_space_corrections = detecter_toute_les_corrections(lettres)


def pretraitement(donnees): # les donnees sont un dictionnaire de session venant des fichier keys
    """
    Rassemble les touches en une seule liste et par lettre.
    donnees : dict{data : list[list[dict]]}
    """
    
    data = donnees["data"]
    data, texte_pour_chaque_mot = unifier_liste(data)
    lettres = group_by_lettre(data)
    lettres.append(texte_pour_chaque_mot)

    return lettres

def write_lettres(lettres, filename, append = True):
    """
    Ecrit les lettres dans un fichier au nom de l'utilisateur
    """
    ## overwrite si user is indentify et si append = False
    ## sinon ajoute au fichier
    lettres_user = []
    tout_les_textes = []
    if (filename != "IDENTIFY.json" and os.path.exists(CHEMIN_DOSSIER_LETTRES + filename)) and append == True:
        lettres_user = load_json(CHEMIN_DOSSIER_LETTRES + filename)
        tout_les_textes = lettres_user[-1]
        lettres_user.pop(-1)

    tout_les_textes += lettres[-1]

    lettres.pop(-1)

    lettres_user += lettres

    lettres_user.append(tout_les_textes)


    with open(CHEMIN_DOSSIER_LETTRES + filename, 'w') as f:
        json.dump(lettres_user, f, indent=4)

def creer_fichier_lettre(donnees, name : str = None, append = True):
    """
    donnees : un dictionnaire de session (1 seule session)
    """
    lettres = pretraitement(donnees)
    if name == None:
        name = donnees["name"]
    write_lettres(lettres, filename=f"{name}.json",append=append)

def from_session_to_lettre(filename, tous = False, name = None, append = True):
    """
    Transforme les fichiers de session en fichiers lettre
    - filename (str) : le nom du fichier json de session
    - name (str) : le nom de la personne. si non renseigné, on prend le premier
    - tous (bool) : si true, on traite toute les session du fichier, quel que soit la variable name
    """
    if tous :
        for session in load_json(CHEMIN_DOSSIER_SESSION + filename):
            creer_fichier_lettre(session,append=append)
    elif name == None : 
        session = load_json(CHEMIN_DOSSIER_SESSION + filename)[0]
        creer_fichier_lettre(session,append=append)
    else : 
        sessions = load_json(CHEMIN_DOSSIER_SESSION + filename, name=name)
        session = list(filter(lambda x : x["name"] == name, sessions))[0]
        creer_fichier_lettre(session, name=name,append=append)