# logic.py
import re

def parse_comment_to_dict(comment):
    """
    Fonction extraite pour être testée unitairement.
    Identifie les listes de choix dans les commentaires SQL du backup MD.
    """
    if not comment: return {}
    text_to_parse = comment.split(', Rubrique')[0]
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