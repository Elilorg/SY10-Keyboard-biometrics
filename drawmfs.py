from data_logic import evaluate_correspondance
from data_logic.lettres_to_user import user_data_from_lettres
from data_logic.keys_to_lettre  import from_session_to_lettre
from data_logic.file_manip import load_lettres, load_json
from data_logic.logs import logger_corres
import logging
from data_logic.membership_functions import IntervalleFlou
import json
import matplotlib.pyplot as plt
if __name__ == "__main__":
   with open("users.json", "r") as f:
      users = json.load(f)
   eliott_user = users.get("Eliott")
   elias_user = users.get("Elias")
   agathe_user = users.get("Agathe")
   identify_user = users.get("IDENTIFY")
   mf1 = eliott_user.get("hold_times").get("A")
   mf2 = elias_user.get("hold_times").get("A")
   mf3 = agathe_user.get("hold_times").get("A")
   mf4 = identify_user.get("hold_times").get("A")
   
   mf1 = IntervalleFlou(*mf1)
   mf2 = IntervalleFlou(*mf2)
   mf3 = IntervalleFlou(*mf3)
   mf4 = IntervalleFlou(*mf4)

   mf1.draw()
   mf2.draw()
   mf3.draw()
   mf4.draw()

   print(mf4.possibilite(mf1))
   print(mf4.possibilite(mf2))
   print(mf4.possibilite(mf3))
   plt.legend(["eliott", "elias","agathe", "identify"])
   plt.show()

