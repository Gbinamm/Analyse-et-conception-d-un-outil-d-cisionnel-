# tests/test_logic.py
from logic import parse_comment_to_dict

def test_parse_enfant_with_parentheses():
    """Vérifie qu'on extrait bien les chiffres et pas le 's' de Enfant(s)"""
    comment = "Enfant(s) à charge (1;2;3;4;5;6;7;8;9;10;11;12;13), Rubrique Usager"
    result = parse_comment_to_dict(comment)
    assert "1" in result
    assert "s" not in result
    assert result["13"] == "13"

def test_parse_mode_with_labels():
    """Vérifie le mapping code:libellé pour le Mode d'entretien"""
    comment = "Mode (1 : RDV; 2 : Sans RDV), Rubrique Entretien"
    result = parse_comment_to_dict(comment)
    assert result["1"] == "RDV"
    assert result["2"] == "Sans RDV"