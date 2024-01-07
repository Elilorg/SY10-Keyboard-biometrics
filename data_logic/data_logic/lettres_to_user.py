from data_logic.file_manip import load_lettres
from data_logic.const import USERS_FILE_PATH, BIGRAMMES,ALPHABET
from data_logic.find_error_by_text import count_all_errors
from data_logic.inter_space_errors import count_all_inter_space_errors
import json
from  data_logic.membership_functions import extract_mf
from data_logic.const import BIGRAMMES
from data_logic.const import SUBSTITUTION
from data_logic.connaissance_clavier import get_connaissance_clavier
from data_logic.run_fis import run_fis


def get_rollover_ratio(lettres):
    """
    Renvoie le ratio de roll over de chaque lettre
    paramètres :
        lettres (dict) : la liste de lettres
    """
    neg_ft_count = 0
    ft_count = 0
    if len(lettres) == 0:
        return 0
    for index, lettre in enumerate(lettres[:-1]):
        if lettre["char"] == "Shift" : 
            continue
        ft = lettres[index+1]["time_pressed"] - lettre["time_released"]
        if ft < 0 : 
            neg_ft_count += 1
        ft_count += 1
    
    return neg_ft_count / ft_count
        
def get_typing_speed(lettres):
    """
    Renvoie la durée totale de saisie (somme des press press time positifs)
    paramètres :
        lettres (dict) : la liste de lettres
    """
    total_time = 0
    for lettre in lettres:
        if 0 < lettre["press_press_time"] < 1000:
            total_time += lettre["press_press_time"]
    return total_time/len(lettres)

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


def update_user_data(users, user_name, data_type, data):
    """
    Crée ou met a jour (écrase) le dictionnaire de l'utilisateur
    paramètres :
        user_name (str) : le nom de l'utilisateur
        data_type {"hold_times"; "flight_times"} : le type de donnée à mettre à jour
        data (dict) : la nouvelle donnée au format dans l'exemple en haut de users.json
        """
    user = users.get(user_name)
    if not user:
        users[user_name] = {}
        user = users[user_name]
    user[data_type] = data
    return users
    


def user_data_from_lettres(user_name, lettres): 
    """
    Ajoute les données (format users.json) d'un utilisateur pour une liste de lettres dans users.json
    paramètres :
        user_name (str) : le nom de l'utilisateur
        lettres (list) : la liste de lettres
        variables (dict) : les variables individuelles collectée durant le process
    """
    # Comptage des erreurs 
    texte_pour_chaque_mot = lettres[-1]
    lettres.pop(-1)
    lettres = [lettre for lettre in lettres if type(lettre) == dict]
    lettres = [lettre for lettre in lettres if lettre["char"] != "Shift"]

    error_count_by_text = count_all_errors(texte_pour_chaque_mot)
    error_count_intserspace  = count_all_inter_space_errors(lettres)

    total_error_count = {}
    for key, value in error_count_by_text.items():
        total_error_count[key] = value + error_count_intserspace[key]


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

    
    
    

    nb_erreurs = sum(total_error_count.values())
    if nb_erreurs == 0:
        error_ratio = 0
        substitution_ratio = 0.055
    else  : 
        error_ratio = nb_erreurs/len(lettres)
        substitution_count = total_error_count[SUBSTITUTION]
        substitution_ratio = substitution_count/nb_erreurs

    typing_speed = get_typing_speed(lettres) 
    print(typing_speed)


    

    # On ajoute le résultat du SIF
    rollover_ratio = get_rollover_ratio(lettres)
    connaissance_clavier = get_connaissance_clavier(lettres)
    if connaissance_clavier != None:
        a1, a2, a3 = connaissance_clavier
    else:
        a1, a2, a3 = 0, 0, 0

    bon, mauvais = run_fis(substitution_ratio, error_ratio, rollover_ratio, typing_speed, a1, a2, a3)

    
    with open(USERS_FILE_PATH, "r") as f:
        users = json.load(f)
    
    users = update_user_data(users,user_name, "hold_times", ht_data)
    users = update_user_data(users, user_name,"flight_times", ft_data)
    users = update_user_data(users, user_name,"bigrammes_hold_times", bg_ht_data)
    users = update_user_data(users, user_name, "indiviual_variables", {
    "error_count" : total_error_count, 
    "error_ratio" : error_ratio, 
    "rollover_ratio" : rollover_ratio,
    "substitution_ratio" : substitution_ratio,
    "typing_speed" : typing_speed,
    "bon" : bon,
    "mauvais" : mauvais
    })

    with open(USERS_FILE_PATH, "w") as f:
        json.dump(users, f, indent=4)
        

if __name__ == "__main__":
    user_data_from_lettres("test1", load_lettres("Elias.json"))