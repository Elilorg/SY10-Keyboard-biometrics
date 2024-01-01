# Biométrie de la dynamique de frappe au clavier
*Projet pour l'UV SY10 - 'Mathématique du floue : concept et application' à l'UTC*
Pour l'ensemble du détail concernant notre projet, merci de vous référer au rapport de projet.

## Résumé

Dans le cadre du projet de semestre, nous avons conçu une application web pour démontrer la faisabilité et l'**utilité** des mathématiques du flou dans l'objectif d'identifier un utilisateur en fonction de son rythme de frappe.
Nous avons de plus ajouté un système flou, pour montrer la compatibilité de notre application avec ce type de système et l'efficacité d'un tel ajout.

## Prérequis
En plus d'installer les packages python contenus dans 'requirements.txt' (avec la commande *pip install -r requirements.txt*), il vous faudra simplement installer Octave pour l'execution du système flou.

## Architecture du projet et execution
### Programme principal
Le site web est basé sur la librairie python 'Flask', et s'execute depuis *main.py* avec la commande :
'''bash
flask --app main.py run --debug
'''

### Logique (floue)

L'intégralité de la logique de l'application, qui permet d'extraire les données utiles, de générer un profil utilisateur et de comparer des profiles entre eux est codée dans les différents fichiers du dossier *data_logic*. Les fonctions de ce dossier sont appelées dans le code principale depuis le fichier *data_treatement.py* Vous y trouverez également tous les fichiers constituants et permettant d'executer le système flou dans *data_logic/octave/*
Les valeurs parametrables sont accessibles dans *data_logic/const.py*.

### Fichiers d'entrée

Le dossier *input/* contient tous les dossiers relatifs aux données récoltées sur les utilisateurs, c'est à dire :
- dans *entire_text*, tout le texte récolté pour chaque utilisateur tel quel.
- dans *session_file*, tous les appuis de touches ainsi que leur temps, en millisecondes depuis l'ouverture de la page
- dans *treated_files*, les fichiers 'lettre' des utilisateurs, soit les appuies regroupés par touche (voir rapport)

Ce dépôt ne contient aucune donnée utilisateur dans un souci de respect des données personnelles. Vous pouvez ajouter des utilisateurs sur la page d'enregistrement.
