from data_logic.file_manip import load_lettres
from data_logic.membership_functions import extract_mf, IntervalleFlou
from data_logic.const import PRCT_NOYAUX_CONAISSANCE_CLAVIER
import numpy as np
#from matplotlib import pyplot as plt

bigrammes_same_hand = [
                        "as", "sa", 
                        "er", "re", 
                        "sd", "ds",
                        "ec", "ce", 
                        "ew", "we", 
                        "wa", "aw", 
                        "cr", "sc", 
                        "cs", "lk", 
                        "lo", "ol", 
                        "op", "po", 
                        "io", "oi", 
                        "no", "on", 
                        "in", "ni"
                        ]

bigramme_hand_alternation = [
                        "al", "la", 
                        "ak", "ka", 
                        "am", "ma", 
                        "an", "na", 
                        "ai", "ia", 
                        "so", "os", 
                        "sp", "ps", 
                        "en", "ne", 
                        "em", "me", 
                        "el", "le", 
                        "ep", "pe"
                        ]

def FT_hands(lettres):
    """
    Renvoie la liste des Flight time pour les bigrammes memes mains et mains différentes
    paramètres :
        lettres (list[dict]) : la liste des lettres
    renvoie :
        FT_sh (list[float]) : la liste des Flight time entre les lettres de même main
        FT_ha (list[float]) : la liste des Flight time entre les lettres de mains différentes
    """
    prec = lettres[0]
    FT_sh = []
    FT_ha = []
    for lettre in lettres[1:]:
        if prec["char"]+lettre["char"] in bigrammes_same_hand:
            FT_sh.append(lettre["time_pressed"]-prec["time_released"])
        if prec["char"]+lettre["char"] in bigramme_hand_alternation:
            FT_ha.append(lettre["time_pressed"]-prec["time_released"])
        prec = lettre
    return [FT_sh, FT_ha]

def possibilite_regles(mf_user: IntervalleFlou):
    """
    Renvoie les degrés de possibilité des 3 classes de la 3eme variable d'entrée de système flou 2
    """
    c1 = IntervalleFlou(100, -100, -1.75, 3, 0.75, "mauvais") # de -20 à -5 dans l'étude
    c2 = IntervalleFlou(100, -0.001, 0.001, 0.5, 0.5, "moyen") 
    c3 = IntervalleFlou(100, 1.75, 100, 0.75, 3, "bon") # de 20 à 28 dans l'étude
    return [c1.possibilite(mf_user), c2.possibilite(mf_user), c3.possibilite(mf_user)]

def get_connaissance_clavier(lettres):
    """
    Renvoie la connaissances clavier d'un utilisateur
    """
    FT_sh, FT_ha = FT_hands(lettres)
    mfsh = IntervalleFlou(*extract_mf(FT_sh, PRCT_NOYAUX_CONAISSANCE_CLAVIER))
    mfha = IntervalleFlou(*extract_mf(FT_ha, PRCT_NOYAUX_CONAISSANCE_CLAVIER))
    if mfha.std_droite is None or mfsh.std_droite is None:
        return None
    mfha.std_droite = mfha.std_droite/3
    mfha.std_gauche = mfha.std_gauche/3
    mfsh.std_droite = mfsh.std_droite/3
    mfsh.std_gauche = mfsh.std_gauche/3
    mfdiff = mfsh-mfha
    print("MDIFF : ", mfdiff)
    #mfsh.draw()
    #mfha.draw()
    #mfdiff.draw()
    #plt.legend()
    #plt.show()

    if mfdiff == None:
        return None
    return possibilite_regles(mfdiff)


if __name__ == "__main__":
    a = load_lettres("Otilia.json")
    b = load_lettres("Eliott.json")
    FT_sh1, FT_ha1 = FT_hands(a)
    mfsh1 = IntervalleFlou(*extract_mf(FT_sh1))
    mfha1 = IntervalleFlou(*extract_mf(FT_ha1))
    FT_sh1 = [x for x in FT_sh1 if abs(x)<500]
    FT_ha1 = [x for x in FT_ha1 if abs(x)<500]
    print(mfsh1.occurrences, np.median(FT_sh1))
    print(mfha1.occurrences, np.median(FT_ha1))

    FT_sh2, FT_ha2 = FT_hands(b)
    mfsh2 = IntervalleFlou(*extract_mf(FT_sh2))
    mfha2 = IntervalleFlou(*extract_mf(FT_ha2))
    print(mfsh2.occurrences)
    print(mfha2.occurrences)

    sub_elias = mfsh1-mfha1
    out = possibilite_regles(sub_elias)
    print(out)



