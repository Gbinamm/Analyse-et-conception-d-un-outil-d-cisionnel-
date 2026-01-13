import pytest
import sys
import os

# Ajustement du chemin pour importer logic.py
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'application')))
from logic import parse_comment_to_dict

def test_parse_enfant_robustness():
    """Vérifie que le parser ignore le (s) de Enfant(s) [cite: 29]"""
    comment = "Enfant(s) à charge (1;2;3;4), Rubrique Usager"
    result = parse_comment_to_dict(comment)
    assert "1" in result
    assert "s" not in result

def test_parse_mode_labels():
    """Vérifie le décodage des modes d'entretien [cite: 21]"""
    comment = "Mode (1 : RDV; 2 : Sans RDV), Rubrique Entretien"
    result = parse_comment_to_dict(comment)
    assert result["1"] == "RDV"
    assert result["2"] == "Sans RDV"