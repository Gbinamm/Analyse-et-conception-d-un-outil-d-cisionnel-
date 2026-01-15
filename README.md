# Téléchargement des packages : 

Pour télécharger les packages, faire : 

pip install -r application/requirements.txt


ou faire : 

pip install -r application/requirements.txt --user

# Lancement du serveur et mise en place de la base de donnée: 

1. Ouvrir l'application pgadmin
2. Démarrer le serveur 
3. Lancer une nouvelle connection avec : 
4. Remplir le fichier avec ces informations : 

        Nom: Choisir un nom  pour la connection 
        Hôte: localhost 
        Port: 5437
        Nom utilisateur: pgis 
        Mot de passe: pgis
5. Création de la base de donnée en faisant un clique droit sur base de données, puis cliquer sur Ajouter une base de données. 

!!! Choisir le nom MD pour la base de données !!! (Pour correspondre avec le paramétrage de l'application python et permet donc un GET et un POST des données)

6. Faire un clique droit sur la base de données précédement crée puis amller sur restaurer et parcourir le dossier de l'application pour se trouver dans 
"H:\SAE_finale\Analyse-et-conception-d-un-outil-d-cisionnel-\base_de_donnee" et prendre le fichier "MaisonDuDroit_bd_avec_donnees_final.backup"

# Insertion des données dans la table entretien, demande à l'aide de la commande : 

 & "D:\tools\pgsql-12.5-win64\bin\psql.exe" -U pgis -d MD -p 5437 -f data.sql

# Insertion des données dans la table solution avec le code  : 
 

SET client_encoding = 'WIN1252';

INSERT INTO public.solution (num, pos, nature) VALUES
(413, 3, '2a'),
(435, 3, '7c'),
(446, 3, '9b'),
(463, 3, '1j'),
(483, 3, '9a'),
(510, 3, '8c'),
(523, 3, '4c'),
(548, 3, '7b'),
(549, 3, '9b'),
(550, 3, '9b'),
(553, 3, '1d'),
(594, 3, '9b'),
(683, 3, '1c'),
(730, 3, '1d'),
(739, 3, '7b'),
(744, 3, '1c'),
(750, 3, '1g'),
(752, 3, '9b'),
(754, 3, '9b');

# Changement de la taille de la variable origine de la table entretien : 

ALTER TABLE public.entretien ALTER COLUMN origine TYPE character varying(50);

# Lancement des test unitaires, web
Pour lancer les test web : 

python test_web/Selenium_test_web.py

Pour lancer les tests unitaires : 

pytest tests_unitaires/ --cov=application


Changement de la base de donnée: 

TRUNCATE TABLE public.demande, public.solution, public.entretien RESTART IDENTITY CASCADE;

