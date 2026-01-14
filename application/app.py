import streamlit as st
import pandas as pd
import psycopg2
from sqlalchemy import create_engine, text 
from datetime import date
import os
import plotly.express as px
import re

# IMPORTATION DE LA LOGIQUE
try:
    from application.logic import parse_comment_to_dict
except ImportError:
    from logic import parse_comment_to_dict

# 1. CONFIGURATION
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
conn_url = f"postgresql://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['dbname']}?client_encoding=win1252"
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
    """Récupère la structure ET les modalités depuis la table 'modalite'"""
    query_cols = f"""
        SELECT a.attname AS column_name, a.attnum as pos,
               format_type(a.atttypid, a.atttypmod) AS data_type,
               col_description(a.attrelid, a.attnum) AS comment, a.attnotnull AS is_required
        FROM pg_attribute a JOIN pg_class c ON a.attrelid = c.oid
        WHERE c.relname = '{table_name.lower()}' AND a.attnum > 0 AND NOT a.attisdropped
        ORDER BY a.attnum;
    """
    try:
        df_cols = pd.read_sql(query_cols, engine)
        structure = []
        for _, row in df_cols.iterrows():
            col_name = row['column_name'].lower()
            if col_name in ['num', 'pos']: continue

            # Récupération des modalités réelles (ex: 1j, 8c...) en base
            query_mod = f"SELECT code, lib_m FROM public.modalite WHERE tab = '{table_name.upper()}' AND pos = {row['pos']} ORDER BY pos_m"
            df_mod = pd.read_sql(query_mod, engine)
            db_choices = dict(zip(df_mod['code'], df_mod['lib_m']))

            config = MANUAL_CONFIG.get(col_name, {})
            comment = row['comment'] or ""
            rubrique = config.get("rubrique", comment.split("Rubrique ")[-1].strip() if "Rubrique " in comment else "Général")
            
            structure.append({
                "name": col_name,
                "display_label": config.get("label", col_name.capitalize()),
                "type": row['data_type'],
                "required": row['is_required'],
                "choices": db_choices if db_choices else parse_comment_to_dict(comment),
                "rubrique": rubrique,
                "full_comment": comment
            })
        return structure
    except Exception: return []

def clean_val_with_meta(col_name, val, metadata):
    """Traduit une valeur brute en utilisant les choix définis dans les métadonnées"""
    val_str = str(val).strip()
    # Recherche de la colonne dans les métadonnées (entretien, demande ou solution)
    col_meta = next((m for m in metadata if m['name'] == col_name.lower()), None)
    
    if col_meta and col_meta['choices']:
        mapping = col_meta['choices']
        if val_str in mapping:
            return mapping[val_str]
    return val_str

def process_var_for_stats(df, col_name, metadata):
    """Prépare les données pour le graphique (gestion des multi-choix '|')"""
    if col_name not in df.columns: return pd.Series()
    temp = df[col_name].dropna().astype(str)
    if temp.str.contains('\|').any():
        temp = temp.str.split('|').explode()
    return temp.apply(lambda x: clean_val_with_meta(col_name, x, metadata))

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
    """Interface utilisateur isolée pour permettre le test de couverture"""
    st.set_page_config(page_title="Maison du Droit", layout="wide")

    # Chargement du style
    local_css("css/style.css")

    if 'choice' not in st.session_state:
        st.session_state.choice = "Ajouter Entretien"

# REMPLACEMENT DU BLOC SIDEBAR (Lignes 186 à 213 environ)
    with st.sidebar:
        st.image("Image/Maison_droit.png", use_container_width=True)
        st.markdown("---")
        
        # Un seul menu Radio pour éviter les conflits dans les tests
        st.markdown(f'<p style="color:#122132; font-weight:bold; margin-bottom:5px;">📂 NAVIGATION</p>', unsafe_allow_html=True)
        
        choice = st.radio(
            "Menu Principal :",
            ["Ajouter Entretien", "Voir Données", "Ajouter Variable", "Modifier Valeurs", "Visualisation"],
            label_visibility="collapsed" # Cache le label pour le style
        )
        
        # On synchronise le choix avec le session_state
        st.session_state.choice = choice

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

    # --- VÉRIFICATION DE SÉCURITÉ ---
    if not struct_ent:
        st.warning("⚠️ Impossible de se connecter à la base de données ou la table est vide.")
        st.stop()

    # --- SECTION : AJOUTER ENTRETIEN ---
    if choice == "Ajouter Entretien":
        with st.form("form_global", clear_on_submit=True):
            # Récupération et tri des rubriques uniques #
            rubriques = sorted(list(set(col['rubrique'] for col in struct_ent)))
            tabs = st.tabs(rubriques + ["Demandes & Solutions"])
            form_data = {}
            
            for i, rub in enumerate(rubriques):
                with tabs[i]:
                    fields = [f for f in struct_ent if f['rubrique'] == rub]
                    cols = st.columns(2)
                    for j, f in enumerate(fields):
                        # Gestion du label (Priorité au display_label défini en Python)
                        label_ui = f"{f.get('display_label', f['name'].capitalize())} {'*' if f['required'] else ''}"
                        curr_col = cols[j % 2]
                        
                        # 1. CAS DES LISTES DÉROULANTES (MODALITÉS)
                        if f['choices']: #
                            sel = curr_col.selectbox(label_ui, list(f['choices'].values()), key=f"ent_{f['name']}")
                            # Récupération du code (ex: '1')
                            val_code = next((k for k, v in f['choices'].items() if v == sel), None)
                            
                            # Conversion forcée si la colonne attend un nombre (smallint/int)
                            if val_code is not None and ('int' in f['type'].lower() or 'serial' in f['type'].lower()):
                                try:
                                    # Nettoyage des apostrophes parasites pour éviter l'erreur SQL
                                    val_code = int(str(val_code).replace("'", "").strip())
                                except ValueError:
                                    pass 
                                    
                            form_data[f['name']] = val_code
                        
                        # 2. CAS DES DATES
                        elif 'date' in f['type']: #
                            form_data[f['name']] = curr_col.date_input(label_ui, key=f"ent_{f['name']}")
                        
                        # 3. CAS DES NOMBRES SAISIS À LA MAIN
                        elif 'int' in f['type'] or 'smallint' in f['type']: #
                            form_data[f['name']] = curr_col.number_input(label_ui, min_value=0, step=1, key=f"ent_{f['name']}")
                        
                        # 4. CAS DU TEXTE LIBRE
                        else: #
                            form_data[f['name']] = curr_col.text_input(label_ui, key=f"ent_{f['name']}")
            
            with tabs[-1]:
                # Gestion des Demandes (Multi-sélection)
                dict_dem = struct_dem[0]['choices'] if struct_dem else {}
                sel_dem = st.multiselect("Natures des Demandes", list(dict_dem.values())) #
                
                # Gestion des Solutions (Multi-sélection)
                dict_sol = struct_sol[0]['choices'] if struct_sol else {}
                sel_sol = st.multiselect("Natures des Solutions", list(dict_sol.values())) #
            
            # Validation finale
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
        if selected_full and " - " in str(selected_full):
            target_tab, target_col = str(selected_full).split(" - ")
        else:
            st.stop() # Arrête proprement si la sélection est invalide
        
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

    # --- SECTION : VISUALISATION (Reporting) ---
    elif choice == "Visualisation":
        st.header("📊 Analyse Statistique")
        
        # Récupération de toutes les données pour l'analyse [cite: 19, 74]
        try:
            df_full = pd.read_sql("SELECT * FROM public.entretien", engine)
            if df_full.empty:
                st.info("Aucune donnée disponible pour l'analyse.")
                st.stop()
        except Exception as e:
            st.error(f"Erreur de lecture BDD : {e}")
            st.stop()

        # Fusion des métadonnées pour avoir accès aux choix de traduction
        all_meta = struct_ent + struct_dem + struct_sol

        # Menu interne comme dans reporting.py
        viz_menu = st.radio("Type d'analyse :", ["Simple", "Croisement"], horizontal=True)

        if viz_menu == "Simple":
            cols_dispo = [c for c in df_full.columns if c not in ["num", "date_ent"]]
            var = st.selectbox("Choisir la variable :", cols_dispo)
            
            if var:
                series = process_var_for_stats(df_full, var, all_meta)
                counts = series.value_counts().reset_index()
                counts.columns = [var, 'Nombre']
                
                c1, c2 = st.columns([2, 1])
                with c1:
                    fig = px.pie(counts, values='Nombre', names=var, title=f"Répartition : {var}", hole=0.4)
                    st.plotly_chart(fig, use_container_width=True)
                with c2:
                    st.dataframe(counts, hide_index=True)

        elif viz_menu == "Croisement":
            c1, c2 = st.columns(2)
            cols_dispo = [c for c in df_full.columns if c not in ["num", "date_ent"]]
            with c1: var1 = st.selectbox("Axe X", cols_dispo, index=0)
            with c2: var2 = st.selectbox("Couleur", cols_dispo, index=min(1, len(cols_dispo)-1))
            
            # Logique de croisement robuste
            clean_rows = []
            for _, row in df_full.iterrows():
                v1_list = str(row[var1]).split('|') if '|' in str(row[var1]) else [str(row[var1])]
                v2_list = str(row[var2]).split('|') if '|' in str(row[var2]) else [str(row[var2])]
                for v1 in v1_list:
                    for v2 in v2_list:
                        if v1.strip() and v2.strip() and v1 != "None" and v2 != "None":
                            clean_rows.append({
                                var1: clean_val_with_meta(var1, v1, all_meta),
                                var2: clean_val_with_meta(var2, v2, all_meta)
                            })
            
            df_cross = pd.DataFrame(clean_rows)
            if not df_cross.empty:
                grouped = df_cross.groupby([var1, var2]).size().reset_index(name='Nombre')
                fig = px.bar(grouped, x=var1, y='Nombre', color=var2, barmode='group', text_auto=True)
                st.plotly_chart(fig, use_container_width=True)

    return choice

if __name__ == "__main__":
    main_ui()