import re

def parse_comment_to_dict(comment):
    """
    Extrait les choix en ignorant les parenthèses de texte comme 'Enfant(s)'.
    Cible spécifiquement les listes de type (1:A; 2:B) ou (1;2;3).
    """
    if not comment: return {}
    
    # Nettoyage : On ignore ce qui vient après ", Rubrique"
    text_to_parse = comment.split(', Rubrique')[0]
    
    # Regex : cherche le contenu entre parenthèses contenant des ';' ou ':'
    matches = re.findall(r'\(([^()]+)\)', text_to_parse)
    
    candidate = None
    for m in matches:
        if ';' in m or ':' in m:
            candidate = m
            break
    
    if not candidate: return {}
            
    mapping = {}
    try:
        items = candidate.split(';')
        for item in items:
            item = item.strip()
            if not item: continue
            if ':' in item:
                parts = item.split(':', 1)
                mapping[parts[0].strip()] = parts[1].strip()
            else:
                mapping[item] = item
        return mapping
    except Exception:
        return {}