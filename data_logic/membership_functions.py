import numpy as np
import matplotlib.pyplot as plt
from data_logic.const import TEMPS_MAXIMAL_AUTORISE, POURCENTAGE_DANS_LE_NOYAUX
from data_logic.logs import logger_intersection
from data_logic.const import NB_OCCURENCE_SUFFISANT, STD_PAR_DEFAUT

class IntervalleFlou:
    def __init__(self,occurrence,  gauche_noyau, droite_noyau, std_gauche, std_droite, username="DEFAULT"):
        self.username = username
        self.gauche_noyau = gauche_noyau
        self.droite_noyau = droite_noyau
        self.std_gauche = std_gauche
        self.std_droite = std_droite
        self.occurrences = occurrence
    
    def draw(self):
        dessiner_fonction_membre(self)
    
    def draw_with(self, other):
        dessiner_deux_fonctions_membre(self.username, other.username, self, other)
    
    def possibilite(self, other):
        return possibilite(self, other)
    
    def __call__(self, x):
        """
        Renvoie la valeur d'appartenance à la mf pour une valeur de x
        """
        return self.appartenance_de(x)

    def appartenance_de(self, x):
        """
        Renvoie la valeur d'appartenance à la mf pour une valeur de x
        """
        # x dans le noyau
        if self.gauche_noyau < x < self.droite_noyau:
            return 1
        
        # x à gauche du noyau
        if x < self.gauche_noyau:
            return np.exp(-(x - self.gauche_noyau)**2 / (2 * self.std_gauche**2)) if self.std_gauche > 0 else 0

        # x à droite du noyau
        if x > self.droite_noyau:
            return np.exp(-(x - self.droite_noyau)**2 / (2 * self.std_droite**2)) if self.std_droite > 0 else 0
        
    def __sub__(self, other):
        """
        Renvoie la soustraction de la mf courante par la mf other
        """
        if self.occurrences == 0 or other.occurrences == 0:
            return None
        occurences = self.occurrences + other.occurrences
        gauche_noyau = self.gauche_noyau - other.droite_noyau  # Erreur askip desfois droite_noyaux c none ? On doit avoir des cas ou y'a zero bigramme faudra enlever ca. 
        droite_noyau = self.droite_noyau - other.gauche_noyau
        std_gauche = self.std_gauche + other.std_gauche
        std_droite = self.std_droite + other.std_droite
        return IntervalleFlou(occurences, gauche_noyau, droite_noyau, std_gauche, std_droite, self.username)

    def __str__(self) -> str:
        return f"username : {self.username}, occurrences : {self.occurrences}, gauche_noyau : {self.gauche_noyau}, droite_noyau : {self.droite_noyau}, std_gauche : {self.std_gauche}, std_droite : {self.std_droite}"




def trouver_intersections(m1,m2,std1,std2):
    """
    Renvoie les 3 racines d'une fonction quadratique
    paramètres :
        m1 (float) : la moyenne de la premiere gaussienne
        m2 (float) : la moyenne de la deuxieme gaussienne
        std1 (float) : l'ecart type de la premiere gaussienne
        std2 (float) : l'ecart type de la deuxieme gaussienne
    """

    a = 1/(2*std1**2) - 1/(2*std2**2)
    b = m2/(std2**2) - m1/(std1**2)
    c = m1**2 /(2*std1**2) - m2**2 / (2*std2**2) 
    return np.roots([a,b,c])

def possibilite(MF1, MF2):
    """
    Renvoie la possibilité entre deux fonctions membres
    paramètres :
        MF1 (MF) : la premiere MF
        MF2 (MF) : la deuxieme MF
    """
    # cas 0 : aucune occurrence
    if MF1.occurrences == 0 or MF2.occurrences == 0:
        return 1

    # cas 1 : intersection des noyaux
    if not ( MF2.droite_noyau < MF1.gauche_noyau or MF1.droite_noyau < MF2.gauche_noyau):
        logger_intersection.info("Intersection des noyaux")
        return 1
    
    # cas 2 : noyau de MF2 a droite de noyau de MF1
    if MF1.droite_noyau < MF2.gauche_noyau:
        logger_intersection.info("Intersection entre MF1 droite et MF2 gauche")
        if MF1.std_droite == 0 or MF2.std_gauche == 0:
            return 0
        intersections = trouver_intersections(MF1.droite_noyau, MF2.gauche_noyau, MF1.std_droite, MF2.std_gauche)
        intersections = [r for r in intersections if r > MF1.droite_noyau and r < MF2.gauche_noyau]
    
    # cas 3 : noyau de MF1 a droite de noyau de MF2
    if MF2.droite_noyau < MF1.gauche_noyau:
        logger_intersection.info("Intersection entre MF1 gauche et MF2 droite")
        if MF1.std_gauche == 0 or MF2.std_droite == 0:
            return 0
        intersections = trouver_intersections(MF1.gauche_noyau, MF2.droite_noyau, MF1.std_gauche, MF2.std_droite)
        intersections = [r for r in intersections if r > MF2.droite_noyau and r < MF1.gauche_noyau]
    
    if len(intersections) == 0:
        raise ValueError("Aucune intersection trouvée, bonne chance pour debugguer ça" + str(MF1) + " et " + str(MF2))
    return MF1.appartenance_de(intersections[0])

def dessiner_fonction_membre(mf):
    """
    Trace la gaussienne en fonction de la moyenne et l'ecart type à gauche et à droite
    Notation Left-Right
    paramètres :
        mf (MF) : la fonction membre
    Attention : n'affiche pas le plot. il faut suivre la fonction de plt.show()
    """

    m1 = mf.gauche_noyau
    m2 = mf.droite_noyau
    std_gauche = mf.std_gauche
    std_droite = mf.std_droite

    x1 = np.linspace(m1 - 3*abs(std_gauche), m1, 500)
    x2 = np.linspace(m1, m2, 100)
    x3 = np.linspace(m2, m2 + 3*abs(std_droite), 500)
    x = np.concatenate((x1, x2, x3))

    y1 = np.exp(-(x1 - m1)**2 / (2 * std_gauche**2)) if std_gauche != 0 else np.zeros(500)
    y2 = np.ones(100)
    y3 = np.exp(-(x3 - m2)**2 / (2 * std_droite**2)) if std_droite != 0 else np.zeros(500)
    y = np.concatenate((y1, y2, y3))

    plt.plot(x, y)

def dessiner_deux_fonctions_membre(user_name1, user_name2, MF1, MF2):
    """
    Trace 2 mfs sur le même graphique
    paramètres :
        user_nameI (str) : le nom du Ieme user
        meanI (float) : la moyenne de l'Ieme user
        stdI (float) : l'ecart type de l'Ieme user
    """
    dessiner_fonction_membre(MF1)
    dessiner_fonction_membre(MF2)
    plt.title("MF compared")
    plt.legend([user_name1, user_name2])
    plt.show()

def extract_mf(data: list, prct_in_kernel=POURCENTAGE_DANS_LE_NOYAUX):
    """
    A partir d'une liste de temps, renvoie le nombre d'occurrences, la moyenne et l'ecart type
    paramètres :
        data (list) : la liste de temps
    renvoie un tuple contenant :
        - le nombre d'occurrences (int)
        - l'abscisse du point gauche du noyau (float)
        - l'abscisse du point droit du noyau (float)
        - l'ecart type de la demi-gaussienne gauche (float)
        - l'ecart type de la demi-gaussienne droite (float)
    """

    data = np.array(data)
    data = data[abs(data)<TEMPS_MAXIMAL_AUTORISE] # exclue les données au dessus de la limite

    occurrences = len(data)

    if occurrences == 0:
        return (0, None, None, None, None)

    # calcul du noyau
    # on prend X% de la donnée pour le noyau

    m1 = np.quantile(data, (1 - prct_in_kernel)/2)
    m2 = np.quantile(data, 1 - (1 - prct_in_kernel)/2)


    # Calcul des écarts types à gauche puis à droite

    d1 = data[data < m1]
    if len(d1) == 0:
        std1 = 0
    else:
        # on ajoute a d1 les valeurs en symétrique par rapport à m1
        sym = m1 - (d1 - m1)
        d1 = np.concatenate([d1, sym])
        # puis on prend la std de ça
        std1 = np.std(d1)

    # pareil pour l'autre coté
    d2 = data[data > m2]
    if len(d2) == 0:
        std2 = 0
    else:
        sym = m2 - (d2 - m2)
        d2 = np.concatenate([d2, sym])
        std2 = np.std(d2)


    # on applique une fonction qui augmente artificiellement la taille
    # du noyau lorsque le nombre de donnée est trop faible
    if occurrences < NB_OCCURENCE_SUFFISANT:
        std1 += (STD_PAR_DEFAUT-occurrences*STD_PAR_DEFAUT/NB_OCCURENCE_SUFFISANT)
        std2 += (STD_PAR_DEFAUT-occurrences*STD_PAR_DEFAUT/NB_OCCURENCE_SUFFISANT)

    retour = [occurrences, m1, m2, std1, std2]
    return [round(x, 3) for x in retour]