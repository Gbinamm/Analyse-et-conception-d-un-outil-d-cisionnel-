Pour télécharger les packages, faire : 

pip install -r application/requirements.txt


ou faire : 

pip install -r application/requirements.txt --user


Pour lancer les test web : 

python test_web/Selenium_test_web.py

Pour lancer les tests unitaires : 

pytest tests_unitaires/ --cov=application


Changement de la base de donnée: 

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
