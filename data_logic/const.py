ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYRÉ'ÈÀ(),.:"

# Liste des bigrammes les plus fréquents
BIGRAMMES = ["ES", "LE", "EN", "RE", "DE", "NT", "TE", "AI", "ET", "ER", "ON", "OU", "SE", "IT", "EL", "AN", "LA","QU", "NE" , "UR" ,"ME", "IE" , "IS" ,"EM"]

# Chemin des différents dossiers qui représentent les étapes de traitement intermédiaires.
USERS_FILE_PATH = "./users.json"
CHEMIN_DOSSIER_SESSION = "./input/session_files/"
CHEMIN_DOSSIER_LETTRES = "./input/treated_files/"

# Temps en ms à partir du quel on ne garde plus la donnée : on concidère que le sujet à été déconcentré
TEMPS_MAXIMAL_AUTORISE = 100

# Nom des différents types d'erreurs
SUBSTITUTION = "substitution"
INSERTION = "insertion"
OMISSION = "omission"

# Nom des différent types de différences repérée par diff patch match
AJOUT = 1 
SUPPRESSION = -1
INCHANGE = 0

# Temps en ms à partir du quel on ne garde plus la donnée : on concidère que le sujet à fait une pause
TEMPS_MAXIMAL_AUTORISE = 1000

COEF = 0.20
POURCENTAGE_DANS_LE_NOYAUX = 0.4
PRCT_NOYAUX_CONAISSANCE_CLAVIER = 0.1

NB_OCCURENCE_SUFFISANT = 10
STD_PAR_DEFAUT = 50

