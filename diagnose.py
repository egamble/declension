
# ------------------
# diagnose.py
# ------------------

import re

def normalize(s: str) -> str:
    """Normalize user input: trim, remove trailing period, collapse spaces."""
    return re.sub(r"\s+", " ", s.strip().rstrip("."))

def diagnose(user_in: str, correct: str, meta: dict) -> str:
    """
    Compare user input against the correct German sentence and expected meta info.
    Returns feedback string with ✅ or ❌ and details.
    """
    ui = normalize(user_in).split()

    # Extract user article/adj/noun
    user_article, user_adj, user_noun = "", "", ""
    if meta["article"]:
        if len(ui) >= 3:
            user_article, user_adj, user_noun = ui[-3], ui[-2], ui[-1]
        elif len(ui) == 2:
            user_adj, user_noun = ui[-2], ui[-1]
        elif len(ui) == 1:
            user_noun = ui[-1]
    else:
        if len(ui) >= 2:
            user_adj, user_noun = ui[-2], ui[-1]
        elif len(ui) == 1:
            user_noun = ui[-1]

    problems = []

    # Article check
    if meta["article"] and user_article.lower() != meta["article"].lower():
        problems.append(f"Article: expected '{meta['article']}', got '{user_article or '∅'}'")

    # Adjective check
    if user_adj.lower() != meta["adj_full"].lower():
        problems.append(f"Adjective: expected '{meta['adj_full']}', got '{user_adj or '∅'}'")

    # Noun check
    if user_noun.lower() != meta["noun_de"].lower():
        problems.append(f"Noun: expected '{meta['noun_de']}', got '{user_noun or '∅'}'")

    # Always append grammar notes
    case_names = {
        "nom": "nominative",
        "acc": "accusative",
        "dat": "dative",
        "gen": "genitive"
    }
    
    case_info = f"(This noun phrase is in the **{case_names[meta['case']]}** case.)"
    decl_info = f"(Declension type: **{meta['declension_type']}**)."

    # ✅ Always show case + declension info, even if correct
    if not problems and normalize(user_in).lower() == normalize(correct).lower():
        return f"✅ Correct!\n{case_info}\n{decl_info}"
    else:
        feedback = ["❌ Not quite.", "Correct: " + correct]
        if problems:
            feedback.append("Details:")
            feedback.extend(" - " + p for p in problems)
        # Add case + declension info at the end
        feedback.append(case_info)
        feedback.append(decl_info)
        return "\n".join(feedback)
