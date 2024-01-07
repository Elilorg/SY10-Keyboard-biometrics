from data_logic.file_manip import load_json, load_lettres
from data_logic.const import USERS_FILE_PATH, BIGRAMMES,ALPHABET
import json
from data_logic.logs import logger_erreurs
from  data_logic.membership_functions import extract_mf
from data_logic.const import BIGRAMMES


def get_HT_lettre(lettres, lettre):
    """
    Renvoie la liste des hold times d'une lettre
    paramètres :
        lettres (dict) : la liste de lettres
        lettre (str) : la lettre (en majuscule) dont on veut les hold times
    """
    return [l["hold_time"] for l in lettres if l["char"].upper() == lettre ]

def get_FT_bigramme(lettres, bigramme:str):
    """
    Récupère les Flight time entre les deux lettres d'un bigramme
    paramètres :
        lettres (list[dict]) : la liste des lettres
        bigramme (str) : le bigramme
    renvoie :
        bigramme_FT (list[float]) : la liste des Flight time
    """
    bigramme_FT = []
    for index, l in enumerate(lettres[:-1]):
        if l["char"].upper() + lettres[index+1]["char"].upper() == bigramme:
            bigramme_FT.append(lettres[index+1]["time_pressed"]-l["time_released"])
    return bigramme_FT

def get_HTs_bigramme(lettres, bigramme: str):
    """
    Renvoie la liste des hold times des lettres d'un bigramme
    paramètres :
        lettres (list[dict]) : la liste des lettres
    renvoie :
        - Un tuple contenant les hold times de chaque lettre du bigramme
    """
    HT_lettre1 = []
    HT_lettre2 = []
    for index, lettre in enumerate(lettres[:-1]):
        if lettre["char"].upper() + lettres[index+1]["char"].upper() == bigramme:
            HT_lettre1.append(lettre["hold_time"])
            HT_lettre2.append(lettres[index+1]["hold_time"])

    return (HT_lettre1, HT_lettre2)


def update_user_data(user_name, data_type, data):
    """
    Crée ou met a jour (écrase) le dictionnaire de l'utilisateur
    paramètres :
        user_name (str) : le nom de l'utilisateur
        data_type {"hold_times"; "flight_times"} : le type de donnée à mettre à jour
        data (dict) : la nouvelle donnée au format dans l'exemple en haut de users.json
        """
    users = load_json(USERS_FILE_PATH)
    user = users.get(user_name)
    if not user:
        users[user_name] = {}
        user = users[user_name]
    user[data_type] = data
    with open(USERS_FILE_PATH, 'w') as f:
        json.dump(users, f, indent=4)
        logger_erreurs.debug(f"Donnée de {user_name} mis à jour pour {data_type}")


def user_data_from_lettres(user_name, lettres): 
    """
    Ajoute les données (format users.json) d'un utilisateur pour une liste de lettres dans users.json
    paramètres :
        user_name (str) : le nom de l'utilisateur
        lettres (list) : la liste de lettres
    """
    ht_data = {}
    for l in ALPHABET:
        ht_data[l] = extract_mf(get_HT_lettre(lettres, l))
    ft_data = {}
    bg_ht_data = {}
    for i, big in enumerate(BIGRAMMES):

        bg_FT = get_FT_bigramme(lettres, big)
        bg_HT = get_HTs_bigramme(lettres, big)

        # flight times
        ft_data[big] = extract_mf(bg_FT) 

        # hold times
        MF_HT_b1 = extract_mf(bg_HT[0])
        MF_HT_b2 = extract_mf(bg_HT[1])
        bg_ht_data[big] = [MF_HT_b1, MF_HT_b2] 

    update_user_data(user_name, "hold_times", ht_data)
    update_user_data(user_name, "flight_times", ft_data)
    update_user_data(user_name, "bigrammes_hold_times", bg_ht_data)

if __name__ == "__main__":
    user_data_from_lettres("test1", load_lettres("Elias.json"))