%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%% Exemple d’algorithme de Zalila
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Copyright © Z. ZALILA & INTELLITECH [intelligent technologies], 2003-2023 –
% All rights reserved
% C. ASSEMAT

%% Algorithme adapté pour notre projet et prévu pour le logiciel Octave

pkg load fuzzy-logic-toolkit; % on charge le package pour le flou

% Initialisation des variables
irr1 = [];
irr2 = [];
irr3 = [];

%% Initialisation des systèmes flous
% chemin en relatif par rapport au fichier python qui appelle
SF1 = readfis('./data_logic/octave/SF1_type_erreur.fis');
SF2 = readfis('./data_logic/octave/SF2_dexterite.fis');
SF3 = readfis('./data_logic/octave/SF3_bon_typer.fis');

%% Récupération des données
arg_list = argv();
var1 = str2num(arg_list{1}); % pourcentage de substitutions [0;1] (cappé à 1)
var2 = str2num(arg_list{2}); % ratio d'erreurs [0;1]
var3 = str2num(arg_list{3}); % rollover ratio [0;1]
var5 = str2num(arg_list{4}); % vitesse de frape [0;200]

% les 3 entrées suivantes sont le tableau de possiblités pour la variable 2 du SF2
possibilites_connaissance_clavier = [str2num(arg_list{5}) str2num(arg_list{6}) str2num(arg_list{7})];

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%%%% Algorithme de Zalila Classification SF1
% On utilise EvalFis
[sortie, irr1, orr, arr] = evalfis([var1, var2], SF1); % odre des args inversé par rapport à matlab
%% On utilise le irr de evalfis : matrice où chaque ligne correspond
%% à une règle, les colonnes représentant leurs prémisses
% ici, le ET et la pseudo-implication sont modélisés par la T-norme
% min. On calcule le degré de déclenchement de chaque règle
declenchementSF1 = min(irr1, [], 2); % min de chaque ligne
%%%%%%%%%%

%% Conséquence floue Finale : par max-union de toutes les conséquences floues
%% partielles
% Initialisation de la conséquence floue finale
nbruleSF1 = length(SF1.rule); % Nombre de règles
nbCsqSF1 = length(SF1.output.mf); % Nombre de classes de sortie
csqSF1 = zeros(1,nbCsqSF1);
for i = 1:nbruleSF1,
  csqSF1(SF1.rule(i).consequent) = max(csqSF1(SF1.rule(i).consequent),...
                                    declenchementSF1(i));
end;
% Affichage de la conséquence floue finale de SF1
% Concaténation de texte
CsqSF1Txt = 'Conséquence SF1 = {';
for i = 1:nbCsqSF1
  CsqSF1Txt = strcat(CsqSF1Txt, '(', ...
        (SF1.output.mf(i).name), ';', num2str(csqSF1(i)), '),');
end
CsqSF1Txt = strcat(CsqSF1Txt(1:end-1), '}');
disp(CsqSF1Txt);

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%% Algorithme de Zalila Classification SF2
%%%% même chose que précédemment
% On utilise EvalFis pour obtenir une base de irr avec les bonnes 
% valeurs pour la première variable
[sortie, irr2, orr, arr] = evalfis([var3, 1], SF2); 

nbruleSF2 = length(SF2.rule); % Nombre de règles
nbCsqSF2 = length(SF2.output.mf); % Nombre de classes de sortie
for i = 1:nbruleSF2, % Boucle sur les règles
  % on rempli l'irr pour la colonne de la seconde variable en fonction
  % des possiblités des classes obtenues en paramètre
  irr2(i,2) = possibilites_connaissance_clavier(SF2.rule(i).antecedent(2));
end;

%% Avec l'irr créé nous pouvons effectuer les mêmes calculs que précédemment
declenchementSF2 = min(irr2, [], 2); % min de chaque ligne
%%%%%%%%%%
%% Conséquence floue Finale : par max-union de toutes les conséquences floues
%% partielles
% Initialisation de la conséquence floue finale
csqSF2 = zeros(1,nbCsqSF2);
for i = 1:nbruleSF2,
  csqSF2(SF2.rule(i).consequent) = max(csqSF2(SF2.rule(i).consequent),...
                                       declenchementSF2(i));
end;
% Affichage de la conséquence floue finale de SF2
% Concaténation de texte
CsqSF2Txt = 'Conséquence SF2 = {';
for i = 1:nbCsqSF2
  CsqSF2Txt = strcat(CsqSF2Txt, '(', ...
       (SF2.output.mf(i).name), ';', num2str(csqSF2(i)), '),');
end
CsqSF2Txt = strcat(CsqSF2Txt(1:end-1), '}');
disp(CsqSF2Txt);

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%%%% Algorithme de Zalila Généralisé SF3
% pas de phase de fuzzification. Il est inutile d'utiliser evalfis
% pour obtenir l'irr, il faut donc créer l'irr à la main 
% il faut aussi ajouter la variable 5
% Pour commencer on évalue le fis avec la variable 5 
% et les autres valeurs à 1 pour trouver la 3eme colonne de l'irr

[sortie_temp, irr_temp, orr_temp, arr_temp] = evalfis([1, 1, var5], SF3);

nbruleSF3 = length(SF3.rule); % Nombre de règles
nbCsqSF3 = length(SF3.output.mf); % Nombre de classes de sortie
for i = 1:nbruleSF3, % Boucle sur les règles
  irr3(i,1) = csqSF1(SF3.rule(i).antecedent(1));
  irr3(i,2) = csqSF2(SF3.rule(i).antecedent(2));
  % on met la 3eme colonne de irr_temp dans la matrice irr3
  irr3(i,3) = irr_temp(i,3);
end;
%% Avec l'irr créé nous pouvons effectuer les mêmes calculs que précédemment
declenchementSF3 = min(irr3, [], 2); % min de chaque ligne

%%%%%%%%%%
%% Conséquence floue Finale : par max-union de toutes les conséquences floues
%% partielles
% Initialisation de la conséquence floue finale
csqSF3 = zeros(1,nbCsqSF3);
for i = 1:nbruleSF3,
  csqSF3(SF3.rule(i).consequent) = max(csqSF3(SF3.rule(i).consequent),...
                                        declenchementSF3(i));
end;
% Affichage de la conséquence floue finale de SF3
% Concaténation de texte
CsqSF3Txt = 'Conséquence SF3 = {';
for i = 1:nbCsqSF3
  CsqSF3Txt = strcat(CsqSF3Txt, '(', ...
       (SF3.output.mf(i).name), ';', num2str(csqSF3(i)), '),');
end
CsqSF3Txt = strcat(CsqSF3Txt(1:end-1), '}');
disp(CsqSF3Txt);
disp('IRR1 :')
disp(irr1)
disp('IRR2 :')
disp(irr2)
disp('IRR3 :')
disp(irr3)