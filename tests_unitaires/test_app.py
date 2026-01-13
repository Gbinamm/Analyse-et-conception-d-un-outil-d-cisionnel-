from streamlit.testing.v1 import AppTest
import sys
import os

# Ajustement du chemin
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'application')))

def test_app_startup():
    """Vérifie le chargement de l'interface"""
    at = AppTest.from_file("application/app.py").run()
    assert at.title[0].value == "⚖️ Gestion Maison du Droit - Vannes"

def test_navigation():
    """Vérifie le changement de page"""
    at = AppTest.from_file("application/app.py").run()
    at.sidebar.radio[0].set_value("Voir Données").run()
    assert at.header[0].value == "Visualisation"