import json
from data_logic.const import CHEMIN_DOSSIER_LETTRES

def load_json(filename : str):
    """
    Charge un fichier json :
        filename (str) : le nom du fichier json
    """
    with open(filename, 'r') as f:
        lettres = json.load(f)
    return lettres

def load_lettres(filename : str):
    """
    Charge un fichier json lettre :
        filename (str) : le nom du fichier json traité. 
    """
    return load_json(CHEMIN_DOSSIER_LETTRES + filename)

def load_session_file(filename : str, name="DEFAULT NAME") : 
    liste = load_json(filename)
    return list(filter(lambda x : x["name"] == name, liste))[0]

if __name__ == "__main__":
    pass