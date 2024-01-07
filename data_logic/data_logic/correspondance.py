from data_logic.file_manip import load_json
from  data_logic.membership_functions import IntervalleFlou
from data_logic.const import USERS_FILE_PATH, BIGRAMMES
from data_logic.logs import log_correspondance, logger_corres, logger_erreurs
from numpy import prod


def evaluate_correspondance(user_name1, user_name2):
    """
    Renvoie le score de correspondance entre deux utilisateurs
    paramètres :
        user_name1 (str) : le nom de l'utilisateur
        user_name2 (str) : le nom de l'utilisateur
    """

    #types de données sur lesquelles effectuer un similarite classique
    classic_types = ["hold_times", "flight_times"]

    user_data = load_json(USERS_FILE_PATH).get(user_name1)
    data_identify = load_json(USERS_FILE_PATH).get(user_name2)
    if not user_data or not data_identify:
        raise ValueError("L'utilisateur n'existe pas")
    similarites = []
    for data_type in classic_types:
        for element in user_data[data_type].keys():
            try:
                mf_user1 = IntervalleFlou(*user_data[data_type][element])
                mf_user2 = IntervalleFlou(*data_identify[data_type][element])
            except KeyError:
                print(f"L'élément {element} n'existe pas dans l'utilisateur {user_name1} ou {user_name2}")
                continue

            if mf_user1.occurrences <= 3 or mf_user2.occurrences <= 3:
                logger_erreurs.info(f"L'élément {element} n'a pas d'occurrence dans l'utilisateur {user_name1} ou {user_name2}")
                continue
            similarites.append(mf_user1.possibilite(mf_user2))
            #print(element, mf_user1.possibilite(mf_user2))
    # evaluation de similarité des HTs des bigrammes avec des ET

    similarites_bigrammes = []
    for bigramme in BIGRAMMES:
        mf1_1, mf1_2 = user_data["bigrammes_hold_times"][bigramme]
        mf1_1, mf1_2 = IntervalleFlou(*mf1_1), IntervalleFlou(*mf1_2)
        mf2_1, mf2_2 = data_identify["bigrammes_hold_times"][bigramme]
        mf2_1, mf2_2 = IntervalleFlou(*mf2_1), IntervalleFlou(*mf2_2)
        mfs = [mf1_1, mf1_2, mf2_1, mf2_2]


        
        if any([mf.occurrences == 0 for mf in mfs]) or any([mf.std_droite == 0 or mf.std_gauche == 0 for mf in mfs]):
            logger_erreurs.info(f"L'élément {bigramme} n'a pas d'occurrence dans l'utilisateur {user_name1} ou {user_name2}")
            continue
        sim1 = mf1_1.possibilite(mf2_1)
        sim2 = mf1_2.possibilite(mf2_2)
        #similarites_bigrammes.append(min(sim1, sim2)) # le ET est un min
        similarites_bigrammes.append(sim1 * sim2) # le ET est un min
    
    ## RESULTATS DU SIF 
    bon1 = user_data["indiviual_variables"]["bon"]
    bon2 = data_identify["indiviual_variables"]["bon"]
    ## IMPLICATION bon1 implique bon2
    implication1 = implication_reichenbach(bon2, bon1)

    mauvais1 = user_data["indiviual_variables"]["mauvais"]
    mauvais2 = data_identify["indiviual_variables"]["mauvais"]

    # IMPLICATION identify mauvais implique user mauvais
    implication2 = implication_reichenbach(mauvais2, mauvais1)

    logger_corres.info(f"Implications : Identify bon => {user_name1} bon : {implication1} ; (resp mauvais) : {implication2}")

    log_correspondance(user_name1, user_name2, prod([prod(similarites) , prod(similarites_bigrammes)])) # De niveau INFO
    logger_corres.debug(f"          {user_name1} {user_name2} HT : {round(prod(similarites), 2)} Big : {round(prod(similarites_bigrammes), 2)}")
    return prod([prod(similarites) , prod(similarites_bigrammes), prod([implication1, implication2])])

def implication_reichenbach(a, b):
    return 1 - a + a*b