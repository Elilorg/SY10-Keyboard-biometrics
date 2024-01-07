import diff_match_patch as dmp_module
from data_logic.const import OMISSION, INSERTION, SUBSTITUTION
from data_logic.const import AJOUT, SUPPRESSION, INCHANGE
from data_logic.logs import logger_corrections
import logging

def filtre(différence) :  # Ne garde que les différences interessantes (pas les trop longues quoi.)
    if différence[0] == 0 : 
        return False
    if len(différence[1]) > 4 : 
        return False



    return True

def trouver_les_différences(textbefore, textafter) : 
    dmp = dmp_module.diff_match_patch()
    dmp.Diff_EditCost = 4
    diff = dmp.diff_main(textbefore, textafter)
    dmp.diff_cleanupSemantic(diff)
    diff = [list(l) for l in diff]
    original = diff.copy()
    
    dernier = diff.pop(-1)
    if len(dernier[1].split(" ")) >= 2 and dernier[0] >= AJOUT and dernier[1].split(" ")[0] != "": 
        diff.append([1, dernier[1].split(" ")[0]])
    for index, difference in enumerate(diff[:-1]) : 
        if difference[0] == SUPPRESSION and diff[index+1][0] == AJOUT : 
            diff[index][0] = -2
            diff[index+1][0] = 2
    diff = list(filter(filtre, diff))
    if len(diff) > 0 : 
        logger_corrections.debug(original)
        logger_corrections.info(diff)
    erreurs_count = count_error_types(diff)
    return erreurs_count
    

def count_error_types(diff) : 
    error_types_count = {
        INSERTION : 0,
        OMISSION : 0,
        SUBSTITUTION : 0
    }
    i = 0
    while i < len(diff) :
        if diff[i][0] == AJOUT  : 
            error_types_count[OMISSION] += 1
            i += 1
        elif diff[i][0] == SUPPRESSION : 
            error_types_count[INSERTION] += 1
            i += 1
        elif diff[i][0] == -2 :
                if i ==  len(diff) - 1 :  # On est déjà à la fin
                    error_types_count[INSERTION] += 1
                    i += 1
                elif diff[i+1][0] == 2 : 
                    error_types_count[SUBSTITUTION] += 1
                    i += 2
        elif diff[i][0] == 2 : 
            error_types_count[OMISSION] += 1
            i += 1
    
    return error_types_count


def count_all_errors(texte_pour_chaque_mot: list[str]) : 
    total_error_count = {
        INSERTION : 0,
        OMISSION : 0,
        SUBSTITUTION : 0
    }

    for index, texte in enumerate(texte_pour_chaque_mot[:-1]) : 
        err_count = trouver_les_différences(texte, texte_pour_chaque_mot[index+1])
        for key, value in err_count.items() : 
            total_error_count[key] += value
    return total_error_count


if __name__ == "__main__":
    mot_replaced = trouver_les_différences(
        "Je suis elas lorgier", 
        "Je suis elias lorgner")
    #print(count_error_types(mot_replaced))



    ## UNE SOLUTION SIMPLE 

