# ┌───────────────────────────────┐
# │                               │
# │    Detecter toutes les        │
# │    corrections                │
# │ ┌───────────────────────────┐ │
# │ │  Detecter corrections mot │ │
# │ │                           │ │
# │ │ ┌──────────────────────── │ │
# │ │ │ EspaceMot.corrections() │ │
# │ │ │                       │ │ │
# │ │ └───────────────────────┘ │ │
# │ │                           │ │
# │ └───────────────────────────┘ │
# │                               │
# └───────────────────────────────┘

#detecter corrections découpe par les espaces 
#
#detecter correction mot découpe en "espace mot"
#
#EspaceMot.corrections() trouve les corrections
from data_logic.find_error_by_text import trouver_les_différences
from data_logic.const import INSERTION, OMISSION, SUBSTITUTION

def analyser_action_mot(mot : list[dict], rindexs : list[int]) -> dict:
    """
    Analyse les actions d'un mot
    C'est ici qu'on detecte les erreurs de substitution, de
    Je devrais aussi renvoyer une différence de longueur après l'écriture de ce mot. 
    """
    if len(mot) <= 3 : 
        return None
    
    mot_final : list[str]= []
    originaux : list[str] = []
    inserting = False  # En cas d'insertion succéssive, évite d'ajouter des originaux a chaque fois
    deleting = False # En cas de suppressions succéssives, evite d'ajouter des originaux a chaque fois
    for index, action in enumerate(mot) : 
        if action["char"] == "Enter" : 
            mot_final.insert(rindexs[index], " ")
        if action["char"] == "Backspace" and len(mot_final)>0 : 
            if not deleting :
                original = "".join(mot_final)
                originaux.append(original)
            try : 
                mot_final.pop(rindexs[index]-1)
            except : 
                print(f"pop index out of range : {rindexs[index] - 1}, in {mot_final}")
            deleting = True

        elif len(action["char"]) == 1: # Est bien un caractère qui ajoute un index quoi 
            if rindexs[index] < len(mot_final)  :
                if deleting :  # on remplace deleting par inserting car c'est une seule modif de supprimer et ecrire a la suite
                    deleting = False
                    inserting = True
                elif not inserting :
                    originaux.append("".join(mot_final))
                    inserting = True
                
            else :   # L'utilisateur ecrit a la fin du mot. 
                inserting = False
            
            mot_final.insert(rindexs[index], action["char"])
            deleting = False
        else : 
            pass # Ici les backspaces quand le mot est vide, les arrows...
    if len(originaux) == 0 : 
        return None
    originaux.append("".join(mot_final))
    return originaux

        
class EspaceMot:

    def __init__(self, debut : int, fin : int) -> None:
        self.debut = debut
        self.fin = fin       
        self.actions = []
        self.relative_indexs = []
        self.mot = ""
    
    def agrandir_a_gauche(self, n : int = -1) :
        #self.relative_indexs = list(map(lambda x : x - n, self.relative_indexs))
        self.debut += n

    def contains_this(self, action : dict) : 
        return self.debut <= action["caret_pos"] <= self.fin + 1

    def décaler(self, n : int = 1) : 
        self.debut += n
        self.fin += n
    
    def ajouter(self, action : dict) :

        self.relative_indexs.append(action["caret_pos"] - self.debut)
        self.actions.append(action)

        tot = 0
        if action["char"] == "Backspace" :
            tot = -1
            if self.debut == action["caret_pos"]: 
                self.agrandir_a_gauche()
            if len(self.mot) > 0 : 
                self.mot = self.mot[:-1]
        elif action["char"] not in ("ArrowLeft", "ArrowRight", "Shift", "ArrowUp", "ArrowDown" ):
            tot = 1
            self.mot += action["char"]
            self.fin += 1
        else : 
            tot = 0
        
        
        return tot

    def corrections(self) :
        mot_final : list[str]= []
        originaux : list[str] = []
        inserting = False  # En cas d'insertion succéssive, évite d'ajouter des originaux a chaque fois
        deleting = False # En cas de suppressions succéssives, evite d'ajouter des originaux a chaque fois
        return analyser_action_mot(self.actions, self.relative_indexs)

    def __lt__(self, other):
        return self.debut < other.debut
    
    def __str__(self) : 
        return "".join([i["char"] for i in self.actions]).replace("Backspace", "<-").replace("ArrowLeft", "<").replace("ArrowRight", ">").replace("Shift", "^")
      


def detecter_correction_mot(lettres_separee : list[dict]) -> list[str]:
    """
    Cette fonction ajoute les actions aux espaces mots
    """
    
    i = 0
    espace_mots =  []
    while len(lettres_separee)>0 : 
        trouve = False
        for espace_mot in espace_mots :
            if trouve :
                espace_mot.décaler(decalage)
                continue
            if espace_mot.contains_this(lettres_separee[0]) : 
                decalage = espace_mot.ajouter(lettres_separee[0])
                lettres_separee.pop(0)
                trouve = True

        if trouve == False : 
            if "Arrow" in lettres_separee[0]["char"] : # On ne crée pas d'espace mot a partir des fleches puisqu'elle n'ecrivent pas
                lettres_separee.pop(0)
                continue    
            espace_mots.append(EspaceMot(lettres_separee[0]["caret_pos"], lettres_separee[0]["caret_pos"]))
            espace_mots.sort()
    corrections = [i.corrections() for i in espace_mots]
    return corrections


def detecter_toute_les_corrections(lettres : list[dict]) -> list[dict]:
    """
    trouve toutes les corrections qui sont faites entre les espaces
    """
    index_des_espaces = [index for index, i in enumerate(lettres) if i["char"] == " "]
    index_pred = 0
    toute_les_corrections = []
    for fin_de_mot in index_des_espaces :
        # Prendre toute les corrections du mot
        corrections = detecter_correction_mot(lettres[index_pred:fin_de_mot])
        for correction in corrections :
            if correction != None :
                toute_les_corrections.append(correction)
        index_pred = fin_de_mot + 1
    
    return toute_les_corrections  




def count_all_inter_space_errors(lettres : list[dict]) -> int:
    """
    Renvoie le nombre d'erreurs d'inter espaces
    """
    total_diff_count = {
        INSERTION : 0,
        OMISSION : 0,
        SUBSTITUTION : 0
    }
    corrections = detecter_toute_les_corrections(lettres)
    for chaine_difference in corrections  : 
        for index, original in enumerate(chaine_difference[:-1]) : 
            nouveau = chaine_difference[index + 1]
            diff_count = trouver_les_différences(original, nouveau)
            for key, value in diff_count.items() : 
                total_diff_count[key] += value
    return total_diff_count
