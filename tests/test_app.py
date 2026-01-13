# tests/test_app.py
from streamlit.testing.v1 import AppTest

def test_app_startup():
    """Vérifie que l'app se lance sans erreur de décodage WIN1252"""
    at = AppTest.from_file("app.py").run()
    # Vérifie que le titre principal est bien affiché
    assert at.title[0].value == "⚖️ Gestion Maison du Droit - Vannes"

def test_sidebar_navigation():
    """Vérifie que le menu latéral fonctionne"""
    at = AppTest.from_file("app.py").run()
    # On clique sur le deuxième bouton radio de la navigation
    at.sidebar.radio[0].set_value("Voir Données").run()
    assert at.header[0].value == "Visualisation"