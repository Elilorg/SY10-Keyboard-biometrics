from data_logic import evaluate_correspondance
from data_logic.lettres_to_user import user_data_from_lettres
from data_logic.keys_to_lettre  import from_session_to_lettre
from data_logic.file_manip import load_lettres
from data_logic.logs import logger_corres
import logging

logger_corres.setLevel(logging.ERROR)

class sessionFile : 
    ELIAS = "keys_elias.json"
    ELIOTT = "keys_eliott.json"
    OTILIA = "keys_otilia.json"

class treatedFile : 
    ELIAS = "Elias.json"
    ELIOTT = "Eliott.json"
    OTILIA = "Otilia.json"
    SARAH = "Sarah.json"
    AGATHE = "Agathe.json"
    CAIO = "Caio.json"

    FILES = [ELIAS, ELIOTT, AGATHE]

FILES = treatedFile.FILES
def generate_all_users_data():
    for f in FILES:
        from_session_to_lettre(f,append=False)
        user_data_from_lettres(f.split(".")[0], load_lettres(f))

def generate_all_datasplit():
    for f in FILES:
        lettres = load_lettres(f)
        part1, part2 = lettres[:len(lettres)//2], lettres[len(lettres)//2:]
        user_data_from_lettres(f.split(".")[0] + "1", part1)
        user_data_from_lettres(f.split(".")[0] + "2", part2)

def compare_all_datasplits():
    pire_différences  = []
    for f1 in FILES:
        files = FILES.copy()
        files.remove(f1)
        name1 = f1.replace(".json", "") + "1"
        name2 = f1.replace(".json", "") + "2"
        true_correspondance = evaluate_correspondance(name1 , name2)
        
        print(f1.split(".")[0] + "1", f1.split(".")[0] + "2", str(round(true_correspondance* 100, 3) ) + "%")
        
        bad_correspondances = []
        for f2 in files:
            name1 = f1.split(".")[0] + "1"
            name2 = f2.split(".")[0] + "2"
            bad_correspondance = evaluate_correspondance(name1 , name2)
            bad_correspondances.append((name2, bad_correspondance))
            #print("    " + name1, name2, str(round(bad_correspondance* 100, 3) ) + "%")
        la_pire = max(bad_correspondances, key=lambda x: x[1])
        pire_différences.append(true_correspondance - la_pire[1])
        print("La pire : ", la_pire[0], str(round(la_pire[1]* 100, 3) ) + "%")
    print("SCORE GENERAL : ", str(round(sum(pire_différences)/len(pire_différences)* 100, 3) ) + "%")

        

def comparer_fichiers(file1, file2):
    f1 = open(file1, "r")
    f2 = open(file2, "r")

    l1 = f1.read()[2:-1]
    l2 = f2.read()[2:-1]

    persons = l1.split("TRUE")
    persons2 = l2.split("TRUE")

    for p1, p2 in zip(persons, persons2):
        lines1 = p1.split("\n")
        lines2 = p2.split("\n")
        
        name1 = lines1[0].split(" ")[0]
        name2 = lines2[0].split(" ")[0]

        #print("Evaluation for")


    


if __name__ == "__main__":
    logger_corres.setLevel(logging.DEBUG)
    from data_logic.file_manip import load_lettres

    generate_all_users_data()


