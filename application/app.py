import streamlit as st
import pandas as pd
import psycopg2
from sqlalchemy import create_engine, text
from datetime import date
import os

# IMPORTATION DE LA LOGIQUE
try:
    from application.logic import parse_comment_to_dict
except ImportError:
    from logic import parse_comment_to_dict

# 1. CONFIGURATION DE LA BASE DE DONNÉES
DB_CONFIG = {
    "dbname": "MD",
    "user": "pgis",
    "password": "pgis", 
    "host": "localhost",
    "port": "5437"
}

# 2. CONFIGURATION MANUELLE DES LIBELLÉS ET MODALITÉS (PYTHON)
# Modifiez ce dictionnaire pour changer les noms dans l'application
MANUAL_CONFIG = {
    "date_ent": {
        "label": "Date de l'entretien",
        "rubrique": "Entretien",
        "choices": None # Indique un champ date
    },
    "mode": {
        "label": "Mode de contact",
        "rubrique": "Entretien",
        "choices": {"1": "RDV Physique", "2": "Sans RDV", "3": "Appel Téléphonique", "4": "Courrier", "5": "E-mail"}
    },
    "duree": {
        "label": "Durée du rendez-vous",
        "rubrique": "Entretien",
        "choices": {"1": "- 15 min", "2": "15-30 min", "3": "30-45 min", "4": "45-60 min", "5": "+ 60 min"}
    },
    "sexe": {
        "label": "Profil de l'usager",
        "rubrique": "Usager",
        "choices": {"1": "Monsieur", "2": "Madame", "3": "Un Couple", "4": "Professionnel"}
    }
}

# Connexion avec encodage WIN1252 pour les accents
conn_url = f"postgresql://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['dbname']}?client_encoding=utf8"
engine = create_engine(conn_url)

def execute_sql(query, params=None):
    """Exécute une commande SQL de modification (DDL)"""
    with engine.connect() as conn:
        conn.execute(text(query), params)
        conn.commit()
    st.cache_data.clear() # Force le rafraîchissement des métadonnées

def local_css(file_name):
    """Charge le fichier CSS externe"""
    if os.path.exists(file_name):
        with open(file_name) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    else:
        st.error(f"⚠️ Fichier {file_name} introuvable.")

@st.cache_data(ttl=60)
def get_table_metadata(table_name):
    query = f"""
        SELECT a.attname AS column_name, format_type(a.atttypid, a.atttypmod) AS data_type,
               col_description(a.attrelid, a.attnum) AS comment, a.attnotnull AS is_required
        FROM pg_attribute a JOIN pg_class c ON a.attrelid = c.oid
        WHERE c.relname = '{table_name.lower()}' AND a.attnum > 0 AND NOT a.attisdropped
        ORDER BY a.attnum;
    """
    try:
        df = pd.read_sql(query, engine)
        structure = []
        for _, row in df.iterrows():
            col_name = row['column_name'].lower()
            if col_name in ['num', 'pos']: continue
            
            comment = row['comment'] or ""
            
            # Intégration de MANUAL_CONFIG [Correction Logique]
            if col_name in MANUAL_CONFIG:
                config = MANUAL_CONFIG[col_name]
                display_label = config.get("label", col_name.capitalize())
                rubrique = config.get("rubrique", "Général")
                # On s'assure d'avoir un dictionnaire vide si choices est None
                choices = config.get("choices") if config.get("choices") is not None else {}
            else:
                display_label = col_name.capitalize()
                rubrique = comment.split("Rubrique ")[-1].strip() if "Rubrique " in comment else "Général"
                choices = parse_comment_to_dict(comment)
            
            structure.append({
                "name": col_name,
                "display_label": display_label,
                "type": row['data_type'],
                "required": row['is_required'],
                "choices": choices,
                "rubrique": rubrique,
                "full_comment": comment
            })
        return structure
    except Exception: return []

def save_data(ent_data, list_dem, list_sol, dict_dem, dict_sol):
    """Enregistre les données dans PostgreSQL"""
    conn = None
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        conn.set_client_encoding('UTF8')
        cur = conn.cursor()
        
        # Insertion dans la table Entretien
        cols = ent_data.keys()
        vals = [ent_data[c] for c in cols]
        query_ent = f"INSERT INTO public.entretien ({', '.join(cols)}) VALUES ({', '.join(['%s']*len(cols))}) RETURNING num"
        cur.execute(query_ent, vals)
        new_id = cur.fetchone()[0]
        
        # Insertion des Demandes Multiples
        for i, val in enumerate(list_dem):
            code_dem = next((k for k, v in dict_dem.items() if v == val), val)
            cur.execute("INSERT INTO public.demande (num, pos, nature) VALUES (%s, %s, %s)", (new_id, i+1, code_dem))
            
        # Insertion des Solutions Multiples
        for i, val in enumerate(list_sol):
            code_sol = next((k for k, v in dict_sol.items() if v == val), val)
            cur.execute("INSERT INTO public.solution (num, pos, nature) VALUES (%s, %s, %s)", (new_id, i+1, code_sol))
            
        conn.commit()
        st.success(f"✅ Dossier n°{new_id} enregistré avec succès !")
    except Exception as e:
        if conn: conn.rollback()
        st.error(f"Erreur SQL : {e}")
    finally:
        if conn: conn.close()

def main_ui():
    """Interface Utilisateur Streamlit"""
    st.set_page_config(page_title="Maison du Droit", layout="wide")

    # Chargement du style
    local_css("css/style.css")

    if 'choice' not in st.session_state:
        st.session_state.choice = "Ajouter Entretien"

    # Sidebar
    with st.sidebar:
        st.image("Image/Maison_droit.png", use_container_width=True)
        st.markdown("---")  # Barre dorée #AD9B6D via CSS
        
        # Section GESTION
        st.markdown(f'<p style="color:#122132; font-weight:bold; margin-bottom:5px;">📁 GESTION</p>', unsafe_allow_html=True)
        if st.button("Ajouter Entretien", use_container_width=True):
            st.session_state.choice = "Ajouter Entretien"
        if st.button("Voir Données", use_container_width=True):
            st.session_state.choice = "Voir Données"
        
        st.markdown("---") # Séparateur doré
        
        # Section ADMINISTRATION
        st.markdown(f'<p style="color:#122132; font-weight:bold; margin-bottom:5px;">⚙️ CONFIGURATION</p>', unsafe_allow_html=True)
        if st.button("Ajouter Variable", use_container_width=True):
            st.session_state.choice = "Ajouter Variable"
        if st.button("Modifier Valeurs", use_container_width=True):
            st.session_state.choice = "Modifier Valeurs"

    # On récupère le choix final
    choice = st.session_state.choice
        
    # Titre principal (classe CSS .main-title)
    st.markdown('<h1 class="main-title">Gestion Maison du Droit - Vannes</h1>', unsafe_allow_html=True)
    
    struct_ent = get_table_metadata("entretien")
    struct_dem = get_table_metadata("demande")
    struct_sol = get_table_metadata("solution")
    
    # ==============================================================================
    # GESTION DE LA NAVIGATION
    # ==============================================================================

    # Vérification de sécurité pour la base de données
    if not struct_ent:
        st.warning("⚠️ Impossible de se connecter à la base de données ou la table est vide.")
        st.stop()

    # --- SECTION : AJOUTER ENTRETIEN ---
    if choice == "Ajouter Entretien":
        with st.form("form_global", clear_on_submit=True):
            # Récupération des rubriques [cite: 17, 21, 25, 37, 39]
            rubriques = sorted(list(set(col['rubrique'] for col in struct_ent)))
            tabs = st.tabs(rubriques + ["Demandes & Solutions"])
            form_data = {}
            
            for i, rub in enumerate(rubriques):
                with tabs[i]:
                    fields = [f for f in struct_ent if f['rubrique'] == rub]
                    cols = st.columns(2)
                    for j, f in enumerate(fields):
                        label_ui = f"{f.get('display_label', f['name'].capitalize())} {'*' if f['required'] else ''}"
                        curr_col = cols[j % 2]
                        
                        if f['choices']:
                            # Choix par liste déroulante [cite: 21, 23, 31, 33]
                            sel = curr_col.selectbox(label_ui, list(f['choices'].values()), key=f"ent_{f['name']}")
                            form_data[f['name']] = next((k for k, v in f['choices'].items() if v == sel), None)
                        
                        elif 'date' in f['type']:
                            # Saisie de date [cite: 17, 20]
                            form_data[f['name']] = curr_col.date_input(label_ui, key=f"ent_{f['name']}")
                        
                        elif 'int' in f['type'] or 'smallint' in f['type']:
                            # Saisie numérique [cite: 18, 25, 29]
                            form_data[f['name']] = curr_col.number_input(label_ui, min_value=0, step=1, key=f"ent_{f['name']}")
                        
                        else:
                            # Saisie texte [cite: 18, 27, 36, 40]
                            form_data[f['name']] = curr_col.text_input(label_ui, key=f"ent_{f['name']}")
            
            with tabs[-1]:
                dict_dem = struct_dem[0]['choices'] if struct_dem else {}
                sel_dem = st.multiselect("Natures des Demandes", list(dict_dem.values())) # [cite: 16]
                dict_sol = struct_sol[0]['choices'] if struct_sol else {}
                sel_sol = st.multiselect("Natures des Solutions", list(dict_sol.values())) # [cite: 58]
            if st.form_submit_button("💾 ENREGISTRER L'ENTRETIEN", use_container_width=True):
                save_data(form_data, sel_dem, sel_sol, dict_dem, dict_sol)

    # --- SECTION : VOIR DONNÉES ---
    elif choice == "Voir Données":
        st.header("Visualisation des derniers entretiens")
        try:
            # Ordre décroissant par numéro [cite: 19, 74]
            df = pd.read_sql("SELECT * FROM public.entretien ORDER BY num DESC", engine)
            st.dataframe(df, use_container_width=True)
        except Exception as e:
            st.error(f"Erreur lors du chargement des données : {e}")

    # ==============================================================================
    # VUE : AJOUTER VARIABLE (Création de colonne SQL)
    # ==============================================================================

    elif choice == "Ajouter Variable":
        st.subheader("Configuration des Variables")
        with st.form("form_add_var"):
            col1, col2 = st.columns(2)
            with col1:
                target_table = st.selectbox("Table cible", ["entretien", "demande", "solution"])
                new_col_name = st.text_input("Nom technique (ex: situation_pro)").lower()
                new_col_label = st.text_input("Libellé affiché (ex: Votre situation)")
            with col2:
                new_col_type = st.selectbox("Type de donnée", ["SMALLINT", "VARCHAR(100)", "DATE", "INTEGER"])
                new_col_rubric = st.text_input("Rubrique (ex: Usager, Entretien)")

            if st.form_submit_button("Créer la variable"):
                if new_col_name and new_col_label:
                    try:
                        # 1. Création de la colonne
                        execute_sql(f"ALTER TABLE public.{target_table} ADD COLUMN {new_col_name} {new_col_type}")
                        # 2. Ajout du commentaire formateur pour l'app [cite: 19, 21, 23]
                        comment_str = f"{new_col_label}, Rubrique {new_col_rubric}"
                        execute_sql(f"COMMENT ON COLUMN public.{target_table}.{new_col_name} IS :txt", {"txt": comment_str})
                        st.success(f"Variable '{new_col_name}' ajoutée avec succès !")
                    except Exception as e:
                        st.error(f"Erreur : {e}")

    # ==============================================================================
    # VUE : MODIFIER VALEURS (Edition des commentaires SQL)
    # ==============================================================================
    elif choice == "Modifier Valeurs":
        st.subheader("Modification des Modalités")
        
        # Sélection de la variable à modifier
        all_vars = []
        for s in struct_ent: all_vars.append(f"entretien - {s['name']}")
        for s in struct_dem: all_vars.append(f"demande - {s['name']}")
        for s in struct_sol: all_vars.append(f"solution - {s['name']}")
        
        selected_full = st.selectbox("Sélectionnez la question à modifier :", all_vars)
        target_tab, target_col = selected_full.split(" - ")
        
        # Récupération des données actuelles
        current_data = next(v for v in (struct_ent if target_tab=="entretien" else struct_dem if target_tab=="demande" else struct_sol) if v['name'] == target_col)
        
        st.write(f"**Rubrique actuelle :** {current_data['rubrique']}")
        
        with st.form("edit_modalities"):
            new_rubric = st.text_input("Changer la Rubrique", value=current_data['rubrique'])
            
            # Gestion des modalités sous forme de texte brut pour simplifier
            # Format attendu par votre parser : "1 : Choix 1; 2 : Choix 2" 
            if current_data['choices']:
                current_choices_str = "; ".join([f"{k} : {v}" for k, v in current_data['choices'].items()])
            else:
                current_choices_str = "" # Pas de modalités pour ce champ (ex: date)
            new_choices_raw = st.text_area("Modalités (format 'code : libellé' séparés par ';')", 
                                         value=current_choices_str,
                                         help="Exemple : 1 : Oui; 2 : Non; 3 : NSP")
            
            if st.form_submit_button("Mettre à jour les modalités"):
                # Reconstruction du commentaire SQL [cite: 16, 21, 58]
                # Note : On garde le libellé d'origine s'il existe dans le commentaire
                base_label = current_data['full_comment'].split("(")[0].split(",")[0]
                final_comment = f"{base_label} ({new_choices_raw}), Rubrique {new_rubric}"
                
                try:
                    execute_sql(f"COMMENT ON COLUMN public.{target_tab}.{target_col} IS :txt", {"txt": final_comment})
                    st.success("Commentaire mis à jour !")
                    st.rerun()
                except Exception as e:
                    st.error(f"Erreur SQL : {e}")

    return choice

if __name__ == "__main__":
    main_ui()