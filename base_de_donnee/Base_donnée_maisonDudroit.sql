-------------------------------------------------------------------------
-- 1. SCHÉMA DE STOCKAGE DES DONNÉES (ENTRETIEN, DEMANDE, SOLUTION)
-------------------------------------------------------------------------

-- Note : Assurez-vous d'être connecté à la base "DB_maison_droit_utf8"
COMMENT ON DATABASE "MD" IS 'Base de données de la maison du droit à Vannes, SAE 501 2025-2026';

DROP TABLE IF EXISTS QUARTIER CASCADE;
DROP TABLE IF EXISTS COMMUNE CASCADE;
DROP TABLE IF EXISTS AGGLO CASCADE;
DROP TABLE IF EXISTS SOLUTION CASCADE;
DROP TABLE IF EXISTS DEMANDE CASCADE;
DROP TABLE IF EXISTS ENTRETIEN CASCADE;

CREATE TABLE ENTRETIEN(
   NUM SERIAL PRIMARY KEY,
   DATE_ENT DATE DEFAULT CURRENT_DATE,
   MODE SMALLINT,
   DUREE SMALLINT,
   SEXE SMALLINT,
   AGE SMALLINT,
   VIENT_PR SMALLINT,
   SIT_FAM VARCHAR(10), -- Augmenté pour sécurité
   ENFANT SMALLINT,
   MODELE_FAM SMALLINT,
   PROFESSION SMALLINT,
   RESS SMALLINT,
   ORIGINE VARCHAR(10), -- Augmenté pour sécurité
   COMMUNE VARCHAR(100),
   PARTENAIRE VARCHAR(100)
);

-- Commentaires d'origine (Source pour l'extraction automatique)
COMMENT ON TABLE ENTRETIEN IS 'La table entretien est l''une des tables de stockage des données';
COMMENT ON COLUMN ENTRETIEN.NUM IS 'Identifiant de l''entretien, Rubrique Entretien';
COMMENT ON COLUMN ENTRETIEN.DATE_ENT IS 'Date de l''entretien, Valeur par défaut : jour courant, Rubrique Entretien';
COMMENT ON COLUMN ENTRETIEN.MODE IS 'Mode de l''entretien (1 : RDV; 2 : Sans RDV;3 : Téléphonique;4 : Courrier;5 : Mail), Rubrique Entretien';
COMMENT ON COLUMN ENTRETIEN.DUREE IS 'Durée de l''entretien (1 : - de 15 min;2 : 15 à 30 min;3 : 30 à 45 min;4 : 45 à 60 min;5 ; + de 60 min), Rubrique Entretien';
COMMENT ON COLUMN ENTRETIEN.SEXE IS 'Sexe (1 : Homme;2 : Femme;3 : Couple;4 : Professionnel), Rubrique Usager';
COMMENT ON COLUMN ENTRETIEN.AGE IS 'Age de la personne (1 : -18 ans;2 : 18-25 ans;3 : 26-40 ans;4 : 41-60 ans;5 : + 60 ans), Rubrique Usager';
COMMENT ON COLUMN ENTRETIEN.VIENT_PR IS 'Vient pour (1 : Soi;2 : Conjoint;3 : Parent;4 : Enfant;5 : Personne morale;6 : Autre), Rubrique Usager';
COMMENT ON COLUMN ENTRETIEN.SIT_FAM IS 'Situation familiale (1 : Célibataire;2 : Concubin;3 : Pacsé;4 : Marié;5 : Séparé/divorcé;5a : Séparé/divorcé Sans enf. à charge;5b : Séparé/divorcé Avec enf. en garde alternée;5c : Séparé/divorcé Avec enf. en garde principale;5d : Séparé/divorcé Avec enf. en droit de visite/hbgt;5e : Séparé/divorcé Parent isolé; 5f : Séparé/divorcé Séparés sous le même toit;6 : Veuf/ve;6a : Veuf/ve Sans enf. à charge;6b : Veuf/ve Avec enf. à charge;7 : Non renseigné), Rubrique Usager';
COMMENT ON COLUMN ENTRETIEN.ENFANT IS 'Enfant(s) à charge (1;2;3;4;5;6;7;8;9;10;11;12;13), Rubrique Usager';
COMMENT ON COLUMN ENTRETIEN.MODELE_FAM IS 'Modèle familial (1 : Famille traditionnelle;2 : Famille monoparentale;3 : Famille recomposée), Rubrique Usager';
COMMENT ON COLUMN ENTRETIEN.PROFESSION IS 'Profession (1 : Scolaire;2 : Pêcheur;3 : Chef entreprise;4 : Libéral;5 : Militaire;6 : Employé;7 : Ouvrier;8 : Cadre;9 : Retraité;10 : Recherche emploi;11 : Sans profession;12 : Non renseigné), Rubrique Usager';
COMMENT ON COLUMN ENTRETIEN.RESS IS 'Revenus (1 : Salaire;2 : Revenus pro.;3 : Retraite;4 : Chômage;5 : RSA;6 : AAH;7 : IJSS;8 : Bourse;9 : Sans revenu;10 : Autre;11 : Non renseigné), Rubrique Usager';
COMMENT ON COLUMN ENTRETIEN.ORIGINE IS 'Origine (1a : Bouche oreille;1b : Internet;1c : Presse;2a : Déjà venu;3a : Tribunaux;4a : CAF;5a : Assistante sociale;6a : France Victimes;7a : Protection juridique;8 : Action collective;9 : 3949), Rubrique Repérage du dispositif';
COMMENT ON COLUMN ENTRETIEN.COMMUNE IS 'Commune de résidence (Allaire;Ambon;Arradon;Arzal;Arzon;Augan;Auray;Auray Gumenen Goaner-Parco Pointer;Baden;Baud;Béganne;Beignon;Belle-Ile;Belz;Berné;Berric;Bieuzy;Bignan;Billers;Billio;Bohal;Brandérion;Brandivy;Brech;Bréhan;Brignac;Bubry;Buléon;Caden;Calan;Camoël;Camors;Campénéac;Carentoir;Carnac;Caro;Caudan;Cléguérec;Cléguers;Colpo;Concoret;Cournon;Crac''h;Crédin;Croixanvec;Cruguel;Damgan;Elven;Erdeven;Etel;Evellys;Evriguet;Férel;Gavres;Glénac;Gestel;Gourhel;Gourrin;Grand-Champ;Guegon;Guéhenno;Gueltas;Guémené-sur-Scorff;Guénin;Guer;Guern;Guidel;Guillac;Guilliers;Guiscriff;Helléan;Hennebont;Ile d''Arz;Ile de Groix;Ile de Hoedic;Ile de Houat;Ile aux Moines;Inguiniel;Inzinzac-Lochrist;Josselin;Kerfourn;Kergrist;Kernascléden;Kervignac;La Chapelle Caro;La Chapelle Gaceline;La Chapelle Neuve;La Croix Helléan;La Gascilly;La Grée-Saint-Laurent;La Roche-Bernard;La Trinité-Porhoët;La Trinité-sur-Mer;La Trinité-Surzur;La Vraie-Croix;Landaul;Landévant;Lanester;Langoëlan;Langonnet;Languidic;Lannouée;Lantillac;Lanvaudan;Lanvénegen;Larmor-Baden;Larmor-Plage;Larré;Lauzach;Le Bono;Le Cours;Le Croisty;Le Faouët;Les Forges de Lannouée;Les Fougerêts;Le Guerno;Le Hézo;Le Roc-Saint-André;Le Saint;Le Sourn;Le Tour-du-Parc;Lignol;Limerzel;Lizio;Locmalo;Locmaria-Grand-Champ;Locmariaquer;Locminé;Locmiquélic;Locoal-Mendon;Locqueltas;Lorient;Loyat;Malensac;Malestroit;Malguénac;Marzan;Mauron;Melrand;Ménéac;Merlevenez;Meslan;Meucon;Missiriac;Mohon;Molac;Monteneuf;Monterblanc;Monterrein;Montertelot;Moréac;Moustoir-Ac;Moustoir-Remungol;Muzillac;Naizin;Néant-sur-Yvel;Neuillac;Nivillac;Nostang;Noyal-Muzillac;Noyal-Pontivy;Péaule;Peillac;Penestin;Persquen;Plaudren;Plescop;Pleucadeuc;Pleugriffet;Ploemel;Ploemeur;Ploërdut;Ploeren;Ploërmel;Plouay;Plougoumelen;Plouharnel;Plouhinec;Plouray;Pluherlin;Plumelec;Pluméliau;Plumelin;Plumergat;Pluneret;Pluvigner;Pont-Scorff;Pontivy;Porcaro;Port-Louis;Priziac;Quelneuc;Questembert;Queven;Quiberon;Quily;Quistinic;Radenac;Réguiny;Réminiac;Remungol;Riantec;Rieux;Rochefort-en-Terre;Rohan;Roudouallec;Ruffiac;Sarzeau;Séglien;Séné;Sérent;Silfiac;St-Abraham;St-Aignan;St-Allouestre;St-Armel;St-Avé;St-Barthélémy;St-Brieuc de Mauron;St-Caradec-Trégomel;St-Congard;St Connec;St-Dolay;St-Gérand;St-Gildas-de-Rhuys;St-Gonnery;St-Gorgon;St-Gravé;St-Guyomard;St-Jacut-les-Pins;St-Jean-Brévelay;St-Jean-la-Poterie;St-Laurent-sur-Oust;St-Léry;St-Malo-de-Beignon;St-Malo-les-Trois-Fontaines;St-Marcel;St-Martin-sur-Oust;St-Nicolas-du-Tertre;St-Nolff;St-Perreux;St-Philibert;St-Pierre-Quiberon;St-Servant;St-Thuriau;St-Tugdual;St-Vincent-sur-Oust;Ste-Anne-d''Auray;Ste-Brigitte;Ste-Hélène;Sulniac;Surzur;Taupont;Tréhillac;Theix-Noyalo;Tréal;Trédion;Treffléan;Tréhoranteuc;Val d''Oust;Vannes;Vannes Bourdonnaye;Vannes Kercado;Vannes Ménimur;HORS 56 Cotes d''Armor;HORS 56 Finistère;HORS 56 Ille et Vilaine;HORS 56 Loire-Atlantique;HORS 56 Autres départements) , Rubrique Résidence';
COMMENT ON COLUMN ENTRETIEN.PARTENAIRE IS 'Partenaire lors de l''entretien (Permanence juridique Vannes;Permanence juridique Auray;Permanence juridique Questembert;Permanence avocat généraliste;Permanence avocat mineurs;Permanence notaire;Permanence conciliateur de justice;Permanence délégué du défenseur des droits), Rubrique Type de partenaire';

CREATE TABLE DEMANDE(
   NUM INTEGER REFERENCES ENTRETIEN(NUM),
   POS SMALLINT,
   NATURE VARCHAR(100) NOT NULL,
   PRIMARY KEY(NUM, POS)
);
COMMENT ON TABLE DEMANDE IS 'La table demande est l''une des tables de stockage des données';
COMMENT ON COLUMN DEMANDE.POS IS 'Identifiant relatif de la demande (1;2;3;4;5;6;7;8;9;10), Rubrique Demande';
COMMENT ON COLUMN DEMANDE.NATURE IS 'Nature de la demande (1a : Droit de la famille / des personnes Union;1b : Droit de la famille / des personnes Séparation / divorce;1c : Droit de la famille / des personnes PA / PC;1d : Droit de la famille / des personnes Droit de garde;1e : Droit de la famille / des personnes Autorité parentale;1f : Droit de la famille / des personnes Filiation adoption;1g : Droit de la famille / des personnes Régimes matrimoniaux;1h : Droit de la famille / des personnes Protection des majeurs;1i : Droit de la famille / des personnes Etat civil;1j : Droit de la famille / des personnes Successions;1k : Droit de la famille / des personnes Assistance éducative;2a : Droit du logement Litiges locatifs;2b : Droit du logement Expulsion;2c : Droit du logement Achat / vente d''un bien;2d : Droit du logement Copropriété;2e : Droit du logement Droit des biens;2f : Droit du logement Construction / urbanisme;2g : Droit du logement Conflit de voisinage;2h : Droit du logement Autre;3a : Droit de la consommation Crédit / reconnaissance de dette;3b : Droit de la consommation Téléphonie / internet;3c : Droit de la consommation Prestation de service;3d : Droit de la consommation Banque / Assurance;3e : Droit de la consommation Surendettement;3f : Droit de la consommation Autre;4a : Autres domaines du droit civil Responsabilité;4b : Autres domaines du droit civil Voies d''exécution;4c : Autres domaines du droit civil Procédure civile;4d : Autres domaines du droit civil Erreur médicale;4e : Autres domaines du droit civil Accident VTM;4f : Autres domaines du droit civil Autre;5a : Droit du travail / affaires / associations Exécution du contrat de travail;5b : Droit du travail / affaires / associations Rupture du contrat de travail;5c : Droit du travail / affaires / associations Droit des affaires / sociétés;5d : Droit du travail / affaires / associations Droit associatif;5e : Droit du travail / affaires / associations Autre;6a : Droit de la protection sociale Aides sociales;6b : Droit de la protection sociale Sécurité sociale;6c : Droit de la protection sociale Retraite;6d : Droit de la protection sociale Cotisations sociales;6e : Droit de la protection sociale Autre;7a : Droit pénal Auteur / mis en cause;7b : Droit pénal Victime;7c : Droit pénal Violences faites aux femmes;7d : Droit pénal Discriminations;7e : Droit pénal Procédure pénale;7f : Droit pénal Autre;8a : Droit administratif Litige avec une administration;8b : Droit administratif Statuts de la fonction publique;8c : Droit administratif Droit des étrangers;8d : Droit administratif Autre;9a : Démarches et formalités Terminologie juridique;9b : Démarches et formalités Aide juridictionnelle;9c : Démarches et formalités Autre), Rubrique Demande';

CREATE TABLE SOLUTION(
   NUM INTEGER REFERENCES ENTRETIEN(NUM),
   POS SMALLINT,
   NATURE VARCHAR(100) NOT NULL,
   PRIMARY KEY(NUM, POS)
);
COMMENT ON TABLE SOLUTION IS 'La table solution est l''une des tables de stockage des données';
COMMENT ON COLUMN SOLUTION.POS IS 'Identifiant relatif de la solution (1;2;3;4;5;6;7;8;9;10), Rubrique Solution';
COMMENT ON COLUMN SOLUTION.NATURE IS 'Nature de la solution (1 : Information;2a : Aide aux démarches Saisine justice internet;2b : Aide aux démarches Aide CAF - ASF;2c : Aide aux démarches Autre démarche;3a : Aide à la rédaction Courrier;3b : Aide à la rédaction Requête;3c : Aide à la rédaction Autre;4a : Orientation professionnel du droit Avocat;4b : Orientation professionnel du droit Avocat mineur;4c : Orientation professionnel du droit Notaire;4d : Orientation professionnel du droit Huissier;4e : Orientation professionnel du droit Tribunal;4f : Orientation professionnel du droit Police / gendarmerie;4g : Orientation professionnel du droit Autre;5a : Orientation MARD Conciliateur de justice;5b : Orientation MARD Délégué du Défenseur des Droits;5c : Orientation MARD Médiation familiale;5d : Orientation MARD Médiation administrative;5e : Orientation MARD Médiation consommation;5f : Orientation MARD Médiation banque / assurance;6a : Orientation administration Mairie / EPCI;6b : Orientation administration DIRECCTE;6c : Orientation administration CAF;6d : Orientation administration Maison France Service;6e : Orientation administration Préfecture;6f : Orientation administration Impôts;6g : Orientation administration Autre;7a : Orientation association Aide aux victimes;7b : Orientation association Accès au Droit;7c : Orientation association ADIL;7d : Orientation association Association de consommateurs;7e : Orientation association Autre;8a : Orientation santé / social Travailleur social;8b : Orientation santé / social Professionnel de santé;8c : Orientation santé / social Professionnel jeunesse;8d : Orientation santé / social Autre;9a : Orientation organisme privé Protection juridique;9b : Orientation organisme privé Autre organisme privé), Rubrique Solution';

COMMENT ON COLUMN DEMANDE.NUM IS 'Clé étrangère vers l''identifiant de l''entretien, Rubrique Entretien';
COMMENT ON COLUMN SOLUTION.NUM IS 'Clé étrangère vers l''identifiant de l''entretien, Rubrique Entretien';

-------------------------------------------------------------------------
-- 2. CRÉATION DES TABLES DE MÉTADONNÉES
-------------------------------------------------------------------------

DROP TABLE IF EXISTS VALEURS_C CASCADE;
DROP TABLE IF EXISTS MODALITE CASCADE;
DROP TABLE IF EXISTS PLAGE CASCADE;
DROP TABLE IF EXISTS VARIABLE CASCADE;
DROP TABLE IF EXISTS RUBRIQUE CASCADE;

CREATE TABLE RUBRIQUE(
   POS SERIAL PRIMARY KEY,
   LIB VARCHAR(50) NOT NULL
);
COMMENT ON TABLE RUBRIQUE IS 'Métadonnées sur les rubriques de l''entretien pour générer les formulaires et les ordres SQL à la volée.';
COMMENT ON COLUMN RUBRIQUE.POS IS 'Position logique de la rubrique lors de la collecte de données';
COMMENT ON COLUMN RUBRIQUE.LIB IS 'Libellé de la rubrique';

INSERT INTO RUBRIQUE (LIB) VALUES 
('Entretien'), 
('Usager'), 
('Demande'), 
('Solution'), 
('Repérage du dispositif'), 
('Résidence'), 
('Type de partenaire');

CREATE TABLE VARIABLE(
   TAB VARCHAR(30),
   POS SMALLINT,
   LIB VARCHAR(50) NOT NULL,
   COMMENTAIRE VARCHAR(4000),
   MOIS_DEBUT_VALIDITE SMALLINT NOT NULL DEFAULT 1,
   MOIS_FIN_VALIDITE SMALLINT NOT NULL DEFAULT 12,
   TYPE_V VARCHAR(15) NOT NULL, -- Taille augmentée pour "CHAINE"
   DEFVAL SMALLINT,
   EST_CONTRAINTE BOOLEAN NOT NULL DEFAULT FALSE,
   POS_R INTEGER NOT NULL,
   RUBRIQUE INTEGER NOT NULL REFERENCES RUBRIQUE(POS),
   PRIMARY KEY(TAB, POS),
   UNIQUE(TAB, LIB)
);
COMMENT ON TABLE VARIABLE IS 'Métadonnées sur les variables pour générer les formulaires et les ordres SQL à la volée';
COMMENT ON COLUMN VARIABLE.TAB IS 'Table de stockage de la variable';
COMMENT ON COLUMN VARIABLE.POS IS 'Position de la variable dans table de stockage';
COMMENT ON COLUMN VARIABLE.LIB IS 'Libellé de la variable dans la table de stockage';
COMMENT ON COLUMN VARIABLE.POS_R IS 'Position de la variable dans sa rubrique';
COMMENT ON COLUMN VARIABLE.COMMENTAIRE IS 'Aide à la signification de la variable';
COMMENT ON COLUMN VARIABLE.MOIS_DEBUT_VALIDITE IS 'Début de la validité de la variable exprimée en numéro de mois dans l''année. Cette limite inférieure est incluse dans la validité. Valeur par défaut : 1';
COMMENT ON COLUMN VARIABLE.MOIS_FIN_VALIDITE IS 'Fin de la validité de la variable exprimée en numéro de mois dans l''année. Cette limite supérieure est incluse dans la validité. Valeur par défaut : 12';
COMMENT ON COLUMN VARIABLE.TYPE_V IS 'Type de la valeur (MOD; NUM; CHAINE)';
COMMENT ON COLUMN VARIABLE.DEFVAL IS 'Position dans les modalités, ou la liste numérique ou valeur par défaut pour la plage numérique';
COMMENT ON COLUMN VARIABLE.EST_CONTRAINTE IS 'Faut il faire un combo box (False) ou une boite de selection (True)';
COMMENT ON COLUMN VARIABLE.RUBRIQUE IS 'Clé étrangère vers l''identifiant de la rubrique';

CREATE TABLE PLAGE(
   TAB VARCHAR(30),
   POS SMALLINT,
   VAL_MIN SMALLINT DEFAULT 0,
   VAL_MAX SMALLINT DEFAULT 128,
   PRIMARY KEY(TAB, POS),
   FOREIGN KEY(TAB, POS) REFERENCES VARIABLE(TAB, POS)
);
COMMENT ON TABLE PLAGE IS 'Métadonnées sur les plages numériques pour générer les formulaires et les ordres SQL à la volée';
COMMENT ON COLUMN PLAGE.TAB IS 'Table de stockage de la variable';
COMMENT ON COLUMN PLAGE.POS IS 'Position de la variable dans table de stockage';
COMMENT ON COLUMN PLAGE.VAL_MIN IS 'Valeur minimale si numérique, valeur par défaut : 0';
COMMENT ON COLUMN PLAGE.VAL_MAX IS 'Valeur maximale si numérique Valeur par defaut : 128';

CREATE TABLE MODALITE(
   TAB VARCHAR(30),
   POS SMALLINT,
   CODE VARCHAR(20), -- Taille augmentée pour éviter l'erreur de longueur
   POS_M SMALLINT NOT NULL,
   LIB_M VARCHAR(100) NOT NULL,
   PRIMARY KEY(TAB, POS, CODE),
   FOREIGN KEY(TAB, POS) REFERENCES VARIABLE(TAB, POS)
);
COMMENT ON TABLE MODALITE IS 'Métadonnées sur les modalités des variables pour générer les formulaires et les ordres SQL à la volée';
COMMENT ON COLUMN MODALITE.TAB IS 'Table de stockage de la variable';
COMMENT ON COLUMN MODALITE.POS IS 'Position de la variable dans table de stockage';
COMMENT ON COLUMN MODALITE.CODE IS 'Identifiant de la modalité';
COMMENT ON COLUMN MODALITE.POS_M IS 'Position permettant un tri pour retrouver l''ordre logique des modalités';
COMMENT ON COLUMN MODALITE.LIB_M IS 'Libellé de la modalité';

CREATE TABLE VALEURS_C(
   TAB VARCHAR(30),
   POS SMALLINT,
   POS_C SMALLINT,
   LIB VARCHAR(100) NOT NULL,
   PRIMARY KEY(TAB, POS, POS_C),
   FOREIGN KEY(TAB, POS) REFERENCES VARIABLE(TAB, POS)
);
COMMENT ON TABLE VALEURS_C IS 'Métadonnées sur les éléments chaîne de caractères d''une liste pour générer les formulaires et les ordres SQL à la volée';
COMMENT ON COLUMN VALEURS_C.TAB IS 'Table de stockage de la variable';
COMMENT ON COLUMN VALEURS_C.POS IS 'Position de la variable dans table de stockage';
COMMENT ON COLUMN VALEURS_C.POS_C IS 'Identifiant de l''élément de la liste';
COMMENT ON COLUMN VALEURS_C.LIB IS 'Libellé de l''élément de la liste';

-------------------------------------------------------------------------
-- 3. REMPLISSAGE AUTOMATIQUE DES MÉTADONNÉES
-------------------------------------------------------------------------

-- Insertion initiale des variables
INSERT INTO VARIABLE (TAB, POS, LIB, COMMENTAIRE, MOIS_DEBUT_VALIDITE, MOIS_FIN_VALIDITE, TYPE_V, DEFVAL, EST_CONTRAINTE, POS_R, RUBRIQUE)
SELECT 
    UPPER(TABLE_NAME), ordinal_position, UPPER(COLUMN_NAME),
    CASE 
        WHEN POSITION('(' IN pg_catalog.col_description(format('%s.%s',isc.table_schema,isc.table_name)::regclass::oid, isc.ordinal_position)) > 0 
        THEN SUBSTRING(pg_catalog.col_description(format('%s.%s',isc.table_schema,isc.table_name)::regclass::oid, isc.ordinal_position), 1, POSITION('(' IN pg_catalog.col_description(format('%s.%s',isc.table_schema,isc.table_name)::regclass::oid, isc.ordinal_position)) - 1)
        ELSE COALESCE(pg_catalog.col_description(format('%s.%s',isc.table_schema,isc.table_name)::regclass::oid, isc.ordinal_position), 'N/A')
    END,
    1, 12, 'MOD', NULL, FALSE, ordinal_position, 1
FROM information_schema.columns isc
WHERE UPPER(TABLE_NAME) IN ('ENTRETIEN','DEMANDE','SOLUTION')
ORDER BY 1,2,3;

-- Mise à jour dynamique des rubriques
UPDATE VARIABLE V SET RUBRIQUE = R.POS
FROM RUBRIQUE R, information_schema.columns isc
WHERE UPPER(isc.TABLE_NAME) = V.TAB AND UPPER(isc.COLUMN_NAME) = V.LIB
AND POSITION(', Rubrique ' IN pg_catalog.col_description(format('%s.%s',isc.table_schema,isc.table_name)::regclass::oid, isc.ordinal_position)) > 0
AND R.LIB = TRIM(SUBSTRING(pg_catalog.col_description(format('%s.%s',isc.table_schema,isc.table_name)::regclass::oid, isc.ordinal_position), POSITION(', Rubrique ' IN pg_catalog.col_description(format('%s.%s',isc.table_schema,isc.table_name)::regclass::oid, isc.ordinal_position))+11));

-- Ajustements spécifiques
UPDATE VARIABLE SET POS_R = POS WHERE TAB='ENTRETIEN' AND RUBRIQUE=1;
UPDATE VARIABLE SET POS_R = POS-4 WHERE TAB='ENTRETIEN' AND RUBRIQUE=2;
UPDATE VARIABLE SET TYPE_V='NUM' WHERE TAB='ENTRETIEN' AND POS=9;
UPDATE VARIABLE SET TYPE_V='CHAINE' WHERE TAB='ENTRETIEN' AND POS IN (14, 15);
INSERT INTO PLAGE (TAB, POS, VAL_MIN, VAL_MAX) VALUES ('ENTRETIEN', 9, 0, 13);

-------------------------------------------------------------------------
-- 4. PARSING RÉCURSIF DES LISTES (CTE RECURSIVE)
-------------------------------------------------------------------------

WITH RECURSIVE stringlist(CHAINE, TAB, POS, POS_C, LIB) AS (
    SELECT 
        split_part(split_part(pg_catalog.col_description(format('%s.%s',isc.table_schema,isc.table_name)::regclass::oid, isc.ordinal_position), '(', 2), ')', 1),
        UPPER(TABLE_NAME)::VARCHAR, isc.ordinal_position::SMALLINT, 1::SMALLINT, 
        split_part(split_part(split_part(pg_catalog.col_description(format('%s.%s',isc.table_schema,isc.table_name)::regclass::oid, isc.ordinal_position), '(', 2), ')', 1), ';', 1)
    FROM information_schema.columns isc
    WHERE UPPER(TABLE_NAME)='ENTRETIEN' AND isc.ordinal_position IN (14, 15)
    UNION ALL
    SELECT 
        CASE WHEN POSITION(';' IN CHAINE) > 0 THEN SUBSTR(CHAINE, POSITION(';' IN CHAINE)+1) ELSE '' END,
        TAB, POS, (POS_C+1)::SMALLINT,
        split_part(SUBSTR(CHAINE, POSITION(';' IN CHAINE)+1), ';', 1)
    FROM stringlist
    WHERE CHAINE LIKE '%;%'
)
INSERT INTO VALEURS_C (TAB, POS, POS_C, LIB)
SELECT TAB, POS, POS_C, TRIM(LIB) FROM stringlist WHERE LIB <> '';

-- Modalités codées (1 : RDV, etc.)
INSERT INTO MODALITE (TAB, POS, CODE, POS_M, LIB_M)
SELECT UPPER(TABLE_NAME), isc.ordinal_position, split_part(TRIM(a.val), ' : ', 1), a.ord, split_part(TRIM(a.val), ' : ', 2)
FROM information_schema.columns isc,
     unnest(string_to_array(split_part(split_part(pg_catalog.col_description(format('%s.%s',isc.table_schema,isc.table_name)::regclass::oid, isc.ordinal_position), '(', 2), ')', 1), ';')) WITH ORDINALITY a(val, ord)
WHERE pg_catalog.col_description(format('%s.%s',isc.table_schema,isc.table_name)::regclass::oid, isc.ordinal_position) LIKE '% : %';

-------------------------------------------------------------------------
-- 5. DONNÉES GÉOGRAPHIQUES (AGGLO ET COMMUNE)
-------------------------------------------------------------------------

CREATE TABLE AGGLO(
   CODE_A SERIAL PRIMARY KEY,
   NOM_A VARCHAR(100) NOT NULL,
   ACRONYME VARCHAR(20) NOT NULL
   -- URL VARCHAR(100)
);
COMMENT ON TABLE AGGLO IS 'Les communautés de communes ou d''agglomération du morbihan Auray Quiberon Terre Atlantique, AQTA (Auray;Auray Gumenen Goaner-Parco Pointer;Belz;Brech;Camors;Carnac;Crac''h;Erdeven;Etel;Ile de Hoedic;Ile de Houat;Landaul;Landévant;La Trinité-sur-Mer;Locmariaquer;Locoal-Mendon;Ploemel;Plouharnel;Pluneret;Plumergat;Pluvigner;Quiberon;Ste-Anne-d''Auray;St-Philibert;St-Pierre-Quiberon) Golfe du Morbihan - Vannes agglomération, Vannes Agglo (Arradon;Arzon;Baden;Brandivy;Colpo;Elven;Grand-Champ;Ile d''Arz;Ile aux Moines;La Trinité-Surzur;Larmor-Baden;Le Bono;Le Hézo;Le Tour-du-Parc;Meucon;Monterblanc;Plaudren;Plescop;Ploeren;Plougoumelen;St-Armel;St-Avé;St-Gildas-de-Rhuys;St-Nolff;Sarzeau;Séné;Sulniac;Theix-Noyalo;Trédion;Treffléan;Vannes;Vannes Bourdonnaye;Vannes Kercado;Vannes Ménimur) Questembert Communauté, Questembert CO. (Questembert;Limerzel;Caden;Malensac;St-Gravé;Rochefort-en-Terre;Pluherlin;Molac;Le Cours;Larré;La Vraie-Croix;Berric;Lauzach) Arc Sud Bretagne, (Ambon;Arzal;Billiers;Damgan;La Roche-Bernard;Le Guerno;Marzan;Muzillac;Nivillac;Noyal-Muzillac;Péaule;St-Dolay) Oust à Brocéliande Communauté, Oust à Broceliande (Augan;Beignon;Bohal;Carentoir;Caro;Cournon;Guer;La Gascilly;Lizio;Malestroit;Missiriac;Monteneuf;Pleucadeuc;Réminiac;Ruffiac;St-Abraham;St-Congard;St-Guyomard;St-Laurent-sur-Oust;St-Malo-de-Beignon;St-Marcel;St-Martin-sur-Oust;St-Nicolas-du-Tertre;Sérent;Tréal) Ploërmel Communauté, (Brignac;Campénéac;Concoret;Cruguel;Évriguet;Les Forges de Lannouée;Gourhel;Guégon;Guillac;Guilliers;Helléan;Josselin;La Croix Helléan;La Grée-Saint-Laurent;La Trinité-Porhoët;Lantillac;Loyat;Mauron;Ménéac;Mohon;Montertelot;Néant-sur-Yvel;Ploërmel;St-Brieuc de Mauron;St-Léry;St-Malo-les-Trois-Fontaines;St-Servant;Taupont;Tréhorenteuc;Val d''Oust)';
COMMENT ON COLUMN AGGLO.CODE_A IS 'Identifiant de la communauté de communes ou d''agglomération';
COMMENT ON COLUMN AGGLO.NOM_A IS 'Nom complet de la communauté de communes ou d''agglomération';
COMMENT ON COLUMN AGGLO.ACRONYME IS 'Acronyme fait des initiales de la communauté de communes ou d''agglomération ou nom court';
-- COMMENT ON COLUMN AGGLO.URL IS 'URL du site de l''agglomération';

INSERT INTO AGGLO (NOM_A, ACRONYME) VALUES 
('Auray Quiberon Terre Atlantique', 'AQTA'),
('Golfe du Morbihan - Vannes agglomération','Vannes Agglo'),
('Questembert Communauté','Questembert CO'),
('Oust à Brocéliande Communauté','Oust à Broceliande'),
('Arc Sud Bretagne','ASB'),
('Ploërmel Communauté','Ploërmel CO');

CREATE TABLE COMMUNE(
   CODE_C SERIAL PRIMARY KEY,
   NOM_C VARCHAR(100) NOT NULL,
   INSEE VARCHAR(5),
   CODE_A INTEGER REFERENCES AGGLO(CODE_A)
);
COMMENT ON TABLE COMMUNE IS 'Les communes du morbihan';
COMMENT ON COLUMN COMMUNE.CODE_C IS 'Identifiant de la commune';
COMMENT ON COLUMN COMMUNE.NOM_C IS 'Nom de la commune';
COMMENT ON COLUMN COMMUNE.INSEE IS 'Code INSEE de la commune pour le recensement de la population';
-- COMMENT ON COLUMN COMMUNE.URL IS 'URL du site de la commune';

INSERT INTO COMMUNE (NOM_C) 
SELECT LIB FROM VALEURS_C WHERE TAB='ENTRETIEN' AND POS=14 AND LIB NOT LIKE 'HORS 56%' AND LIB NOT LIKE 'Vannes %';

UPDATE COMMUNE SET CODE_A=1 WHERE NOM_C IN ('Auray','Belz','Brech','Camors','Carnac','Crac''h','Erdeven','Etel','Ile de Hoedic','Ile de Houat','Landaul','Landévant','La Trinité-sur-Mer','Locmariaquer','Locoal-Mendon','Ploemel','Plouharnel','Pluneret','Plumergat','Pluvigner','Quiberon','Ste-Anne-d''Auray','St-Philibert','St-Pierre-Quiberon');
UPDATE COMMUNE SET CODE_A=2 WHERE NOM_C IN ('Arradon','Arzon','Baden','Brandivy','Colpo','Elven','Grand-Champ','Ile d''Arz','Ile aux Moines','La Trinité-Surzur','Larmor-Baden','Le Bono','Le Hézo','Le Tour-du-Parc','Meucon','Monterblanc','Plaudren','Plescop','Ploeren','Plougoumelen','St-Armel','St-Avé','St-Gildas-de-Rhuys','St-Nolff','Sarzeau','Séné','Sulniac','Theix-Noyalo','Trédion','Treffléan','Vannes');
UPDATE COMMUNE SET CODE_A=3 WHERE NOM_C IN ('Questembert','Limerzel','Caden','Malensac','St-Gravé','Rochefort-en-Terre','Pluherlin','Molac','Le Cours','Larré','La Vraie-Croix','Berric','Lauzach');
UPDATE COMMUNE SET CODE_A=4 WHERE NOM_C IN ('Augan','Beignon','Bohal','Carentoir','Caro','Cournon','Guer','La Gascilly','Lizio','Malestroit','Missiriac','Monteneuf','Pleucadeuc','Réminiac','Ruffiac','St-Abraham','St-Congard','St-Guyomard','St-Laurent-sur-Oust','St-Malo-de-Beignon','St-Marcel','St-Martin-sur-Oust','St-Nicolas-du-Tertre','Sérent','Tréal');
UPDATE COMMUNE SET CODE_A=5 WHERE NOM_C IN ('Ambon','Arzal','Billiers','Damgan','La Roche-Bernard','Le Guerno','Marzan','Muzillac','Nivillac','Noyal-Muzillac','Péaule','St-Dolay');
UPDATE COMMUNE SET CODE_A=6 WHERE NOM_C IN ('Brignac','Campénéac','Concoret','Cruguel','Évriguet','Les Forges de Lannouée','Gourhel','Guégon','Guillac','Guilliers','Helléan','Josselin','La Croix Helléan','La Grée-Saint-Laurent','La Trinité-Porhoët','Lantillac','Loyat','Mauron','Ménéac','Mohon','Montertelot','Néant-sur-Yvel','Ploërmel','St-Brieuc de Mauron','St-Léry','St-Malo-les-Trois-Fontaines','St-Servant','Taupont','Tréhorenteuc','Val d''Oust');

CREATE TABLE QUARTIER(
   CODE_Q SERIAL PRIMARY KEY,
   NOM_Q VARCHAR(100) NOT NULL,
   CODE_C INTEGER REFERENCES COMMUNE(CODE_C)
);
COMMENT ON TABLE QUARTIER IS 'Liste des quartiers prioritaires en 2025 dans le morbihan hors la zone de Lorient';
COMMENT ON COLUMN QUARTIER.CODE_Q IS 'Identifiant du quartier prioritaire';
COMMENT ON COLUMN QUARTIER.NOM_Q IS 'Nom complet du quartier prioritaire';
-- COMMENT ON COLUMN QUARTIER.INSEE_IRIS IS 'Ménimur (QN05609M), Kercado (QN05608M), Bourdonnaye(), Gumenen Goaner-Parco Pointer (QN05601M)  https://www.insee.fr/fr/outil-interactif/7737357/map.html';


INSERT INTO QUARTIER(NOM_Q, CODE_C) 
SELECT LIB, (SELECT CODE_C FROM COMMUNE WHERE NOM_C='Vannes' LIMIT 1)
FROM VALEURS_C WHERE LIB LIKE 'Vannes %';

-------------------------------------------------------------------------
-- 6. TESTS FINAUX
-------------------------------------------------------------------------

SELECT * FROM VARIABLE ORDER BY TAB, POS;

-- Vérification du parsing (Ligne 435 corrigée)
SELECT 
    split_part(split_part(pg_catalog.col_description(format('%s.%s',table_schema,table_name)::regclass::oid, ordinal_position)::TEXT, '(', 2), ')', 1) as ListContent, 
    table_name as TableName
FROM information_schema.columns
WHERE UPPER(table_name)='ENTRETIEN' AND ordinal_position=15;