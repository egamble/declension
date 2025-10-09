
# ------------------
# feedback.py
# ------------------

import re
from vocabulary import dat_prepositions, acc_prepositions

def normalize(s):
    return re.sub(r"\s+"," ",s.strip().rstrip("."))

def diagnose(user_in, correct, meta):
    ui=normalize(user_in).split()

    prepositions=[p[0] for p in dat_prepositions+acc_prepositions]
    if ui and ui[0] in prepositions:
        ui=ui[1:]

    user_article,user_adj,user_noun="","",""
    if meta["article"]:
        if len(ui)>=3:
            user_article,user_adj,user_noun=ui[-3],ui[-2],ui[-1]
        elif len(ui)==2:
            user_adj,user_noun=ui[-2],ui[-1]
        elif len(ui)==1:
            user_noun=ui[-1]
    else:
        if len(ui)>=2:
            user_adj,user_noun=ui[-2],ui[-1]
        elif len(ui)==1:
            user_noun=ui[-1]

    problems=[]
    if meta["article"] and user_article!=meta["article"]:
        problems.append(f"Article: expected '{meta['article']}', got '{user_article or '∅'}'")
    if user_adj.lower()!=meta["adj_full"].lower():
        problems.append(f"Adjective: expected '{meta['adj_full']}', got '{user_adj or '∅'}'")
    if user_noun.lower()!=meta["noun_de"].lower():
        problems.append(f"Noun: expected '{meta['noun_de']}', got '{user_noun or '∅'}'")

    case_names = {
        "nom": "nominative",
        "acc": "accusative",
        "dat": "dative",
        "gen": "genitive"
    }

    problems.append(f"(This noun phrase is in the **{case_names[meta['case']]}** case.)")
    problems.append(f"(Declension type: **{meta['declension_type']}**).")

    if not problems and normalize(user_in)==normalize(correct):
        return "✅ Correct!"
    else:
        feedback=["❌ Not quite.","Correct: "+correct]
        if problems:
            feedback.append("Details:")
            feedback.extend(" - "+p for p in problems)
        return "\n".join(feedback)
