from data_logic.keys_to_lettre import creer_fichier_lettre
from data_logic.lettres_to_user import user_data_from_lettres
from data_logic.correspondance import evaluate_correspondance



# ┌───────────────┐   ┌───────────────────────┐
# │Session files  ├──>┤from_session_to_lettre ├───┐
# ├───────────────┤   └───────────────────────┘   │
# │Events         │                               │
# │- caret pos    │         ┌──────────────┐      │
# │- timestamp    │         │Treated files │◄─────┘
# │- char         │         ├──────────────┤
# │- pressed or   │         │Lettres       │
# │  released     │ ┌───────┤- press time  │
# └───────────────┘ │       │- release time│
#                   │       │- flight time │
#   ┌───────────────┘       │- char        │
#   │                       └──────────────┘
#   │
# ┌─▼────────────────────┐   ┌─────────────────┐        ┌─────────┐
# │user_data_from_lettres├──>┤users_files      ├───────>┤identify │
# └──────────────────────┘   ├─────────────────┤        └─────────┘
#                            │Lettres          │
#                            │- std left       │
#                            │- std right      │
#                            │- gauche noyaux  │
#                            │- droite noyaux  │
#                            │Bigrammes        │
#                            │- pareil         │
#                            │Erreurs          │
#                            │- omissions      │
#                            │- insertion      │
#                            │- substitution   │
#                            │Variable indiv   │
#                            │- Rollover ratio │
#                            │- Error ratio    │
#                            │- MF conaissance │
#                            │clavier          │
#                            │- Vitesse de     │
#                            │frappe           │
#                            └─────────────────┘             