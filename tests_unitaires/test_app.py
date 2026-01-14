import pytest
import pandas as pd
from unittest.mock import MagicMock, patch
import streamlit as st
import os

# 1. MOCK SESSION STATE AVEC ACCÈS PAR ATTRIBUT
class MockSessionState(dict):
    def __getattr__(self, item): return self.get(item)
    def __setattr__(self, key, value): self[key] = value

mock_cache = MagicMock()
mock_cache.clear = MagicMock()
mock_cache.return_value = lambda f: f

# Neutralisation du cache Streamlit avant l'import
with patch('streamlit.cache_data', mock_cache):
    import application.app as app

# ==============================================================================
# TESTS DES FONCTIONS UNITAIRES (LOGIQUE)
# ==============================================================================

def test_local_css_logic(tmp_path):
    """Couvre le succès et l'erreur de chargement CSS"""
    with patch('application.app.st.error') as mock_err:
        app.local_css("inexistant.css")
        assert mock_err.called
    css = tmp_path / "style.css"
    css.write_text("body {}")
    with patch('application.app.st.markdown') as mock_md:
        app.local_css(str(css))
        assert mock_md.called

@patch('application.app.engine')
def test_execute_sql_logic(mock_engine):
    mock_conn = MagicMock()
    mock_engine.connect.return_value.__enter__.return_value = mock_conn
    app.execute_sql("SELECT 1")
    assert mock_conn.execute.called

def test_stats_logic():
    """Teste le split '|' et le nettoyage des données pour les graphiques"""
    df = pd.DataFrame({'col': ['1|2', '1', None]})
    meta = [{"name": "col", "choices": {"1": "A", "2": "B"}}]
    res = app.process_var_for_stats(df, 'col', meta)
    assert len(res) == 3 # '1', '2', '1'
    assert "A" in res.values

@patch('application.app.psycopg2.connect')
def test_save_data_logic(mock_connect):
    """Couvre l'insertion SQL, commit et rollback"""
    mock_conn = MagicMock()
    mock_connect.return_value = mock_conn
    mock_cur = mock_conn.cursor.return_value
    mock_cur.fetchone.return_value = [101]
    
    # Cas succès
    app.save_data({"m": 1}, ["D1"], ["S1"], {"1": "D1"}, {"1": "S1"})
    assert mock_conn.commit.called
    
    # Cas erreur
    mock_cur.execute.side_effect = Exception("Erreur")
    with patch('application.app.st.error'):
        app.save_data({}, [], [], {}, {})
    assert mock_conn.rollback.called

# ==============================================================================
# TESTS D'INTERFACE (main_ui) - DÉCOUPAGE PAR BRANCHE
# ==============================================================================

@pytest.fixture
def base_ui_mocks():
    """Prépare les mocks de base pour main_ui"""
    with patch('application.app.st') as mock_st, \
         patch('application.app.get_table_metadata') as mock_get_meta, \
         patch('application.app.pd.read_sql') as mock_read_sql:
        
        mock_st.session_state = MockSessionState({'choice': 'Ajouter Entretien'})
        mock_st.columns.return_value = [MagicMock(), MagicMock()]
        mock_st.tabs.return_value = [MagicMock(), MagicMock(), MagicMock()]
        
        # Mocks essentiels pour éviter le TypeError: NoneType object has no attribute values
        meta_ent = [{"name": "m", "choices": {"1":"A"}, "rubrique": "R1", "type": "int", "required": True, "full_comment": "C"}]
        meta_dem = [{"name": "nature", "choices": {"1": "D"}}] # Doit avoir des 'choices'
        meta_sol = [{"name": "nature", "choices": {"1": "S"}}] # Doit avoir des 'choices'
        mock_get_meta.side_effect = [meta_ent, meta_dem, meta_sol] * 5
        
        yield mock_st, mock_get_meta, mock_read_sql

def test_ui_ajouter_entretien(base_ui_mocks):
    mock_st, _, _ = base_ui_mocks
    mock_st.radio.return_value = "Ajouter Entretien"
    mock_st.form_submit_button.return_value = True
    with patch('application.app.save_data'):
        app.main_ui()
        assert mock_st.form.called

def test_ui_visualisation_croisement(base_ui_mocks):
    mock_st, _, mock_read_sql = base_ui_mocks
    mock_st.session_state.choice = "Visualisation"
    # Sidebar puis menu interne
    mock_st.radio.side_effect = ["Visualisation", "Croisement"]
    mock_read_sql.return_value = pd.DataFrame({'m': ['1'], 'sexe': ['2']})
    # Deux noms différents pour l'axe X et la Couleur
    mock_st.selectbox.side_effect = ["m", "sexe"]
    app.main_ui()
    assert mock_st.plotly_chart.called

def test_ui_modifier_valeurs(base_ui_mocks):
    mock_st, _, _ = base_ui_mocks
    mock_st.session_state.choice = "Modifier Valeurs"
    mock_st.radio.return_value = "Modifier Valeurs"
    mock_st.selectbox.return_value = "entretien - m"
    mock_st.form_submit_button.return_value = True
    with patch('application.app.execute_sql'), patch('application.app.st.rerun'):
        app.main_ui()
    assert mock_st.success.called

def test_ui_ajouter_variable(base_ui_mocks):
    mock_st, _, _ = base_ui_mocks
    mock_st.session_state.choice = "Ajouter Variable"
    mock_st.radio.return_value = "Ajouter Variable"
    mock_st.form_submit_button.return_value = True
    mock_st.text_input.return_value = "nom_technique"
    with patch('application.app.execute_sql'):
        app.main_ui()
    assert mock_st.success.called

def test_ui_voir_donnees_error(base_ui_mocks):
    mock_st, _, mock_read_sql = base_ui_mocks
    mock_st.session_state.choice = "Voir Données"
    mock_st.radio.return_value = "Voir Données"
    mock_read_sql.side_effect = Exception("Crash")
    app.main_ui()
    assert mock_st.error.called

def test_ui_security_stop(base_ui_mocks):
    mock_st, mock_get_meta, _ = base_ui_mocks
    mock_get_meta.side_effect = None
    mock_get_meta.return_value = []
    app.main_ui()
    assert mock_st.warning.called

def test_ui_form_numeric_apostrophe_cleaning(base_ui_mocks):
    """Vérifie la logique de nettoyage des apostrophes pour les codes numériques"""
    mock_st, mock_get_meta, _ = base_ui_mocks
    # On simule un choix SQL qui contiendrait des apostrophes (ex: '1')
    meta_num = [{"name": "mode", "type": "int", "choices": {"'1'": "RDV"}, "rubrique": "R1", "required": False}]
    mock_get_meta.side_effect = [meta_num, [], []]
    mock_st.radio.return_value = "Ajouter Entretien"
    
    # Simulation du retour du selectbox (on choisit le libellé "RDV")
    cols = mock_st.columns.return_value
    cols[0].selectbox.return_value = "RDV"
    
    # L'exécution ne doit pas lever d'erreur lors de l'appel à int()
    app.main_ui()

def test_ui_modifier_valeurs_no_modalities(base_ui_mocks):
    """Teste Modifier Valeurs pour un champ n'ayant pas de modalités (ex: date)"""
    mock_st, mock_get_meta, _ = base_ui_mocks
    # AJOUT de 'full_comment' pour éviter le KeyError
    meta_date = [{"name": "date_ent", "choices": None, "rubrique": "R1", "full_comment": "Date de l'entretien"}]
    mock_get_meta.side_effect = [meta_date, [], []]
    mock_st.session_state.choice = "Modifier Valeurs"
    mock_st.radio.return_value = "Modifier Valeurs"
    mock_st.selectbox.return_value = "entretien - date_ent"
    
    # On simule aussi le clic sur le bouton pour couvrir la logique de mise à jour
    mock_st.form_submit_button.return_value = True
    with patch('application.app.execute_sql'), patch('application.app.st.rerun'):
        app.main_ui()
    
    # Vérifie que la zone de texte pour les modalités était bien vide
    # On cherche l'appel à text_area
    found_empty_val = False
    for call in mock_st.text_area.call_args_list:
        if call[1].get('value') == "":
            found_empty_val = True
    assert found_empty_val
def test_ui_form_various_inputs(base_ui_mocks):
    """Teste les différents types d'entrées (Date, Int, Text) dans le formulaire"""
    mock_st, mock_get_meta, _ = base_ui_mocks
    meta_various = [
        {"name": "d", "type": "date", "choices": None, "required": False, "rubrique": "R1", "full_comment": "D"},
        {"name": "n", "type": "int", "choices": None, "required": False, "rubrique": "R1", "full_comment": "N"},
        {"name": "t", "type": "text", "choices": None, "required": False, "rubrique": "R1", "full_comment": "T"}
    ]
    mock_get_meta.side_effect = [meta_various, [], []]
    mock_st.radio.return_value = "Ajouter Entretien"
    app.main_ui()
    # On vérifie que les composants ont été appelés sur les colonnes
    cols = mock_st.columns.return_value
    assert cols[0].date_input.called
    assert cols[1].number_input.called
    assert cols[0].text_input.called

def test_ui_visualisation_simple_mode(base_ui_mocks):
    """Teste la branche Visualisation 'Simple' (graphique Pie)"""
    mock_st, _, mock_read_sql = base_ui_mocks
    mock_st.session_state.choice = "Visualisation"
    # Sidebar selection puis choix interne 'Simple'
    mock_st.radio.side_effect = ["Visualisation", "Simple"]
    mock_read_sql.return_value = pd.DataFrame({'m': ['1', '1']})
    mock_st.selectbox.return_value = "m"
    app.main_ui()
    assert mock_st.plotly_chart.called   

@patch('application.app.pd.read_sql')
@patch('application.app.engine')
def test_get_table_metadata_error_case(mock_engine, mock_read_sql):
    """Teste la sécurité si la requête de structure SQL échoue"""
    mock_read_sql.side_effect = Exception("Database Down")
    result = app.get_table_metadata("entretien")
    assert result == [] # Doit renvoyer une liste vide en cas d'erreur

def test_main_ui_form_else_text_input(base_ui_mocks):
    """Teste la création d'un champ texte libre (branche else)"""
    mock_st, mock_get_meta, _ = base_ui_mocks
    # Type inconnu pour forcer le passage dans le else final du formulaire
    meta_text = [{"name": "comm", "type": "unknown_type", "choices": None, "required": False, "rubrique": "R1"}]
    mock_get_meta.side_effect = [meta_text, [], []]
    mock_st.radio.return_value = "Ajouter Entretien"
    app.main_ui()
    # Vérifie que text_input a été appelé sur l'objet colonne
    cols = mock_st.columns.return_value
    assert cols[0].text_input.called

