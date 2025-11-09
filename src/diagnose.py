# ------------------
# diagnose.py
# ------------------

import re

def normalize(s: str) -> str:
    """Normalize user input:
    - trim, remove trailing period, collapse spaces
    - convert ae/oe/ue to ä/ö/ü (only when not part of real vowel sequence)
    - convert sss to ß (ASCII replacement)
    - preserve capitalization (Ae -> Ä, Ue -> Ü, Sss -> ß)
    """
    s = s.strip().rstrip(".")
    s = re.sub(r"\s+", " ", s)

    # Vowels to check for "not preceded by a vowel"
    vowel_class = "aeiouyäöüAEIOUYÄÖÜ"

    def repl_factory(replacement_lower):
        """Preserve capitalization when replacing."""
        def repl(match):
            text = match.group(0)
            # Uppercase if first letter is uppercase
            if text[0].isupper():
                return replacement_lower.upper()
            return replacement_lower
        return repl

    # Replace ae/oe/ue → ä/ö/ü when NOT preceded by another vowel
    s = re.sub(rf"(?<![{vowel_class}])ae", repl_factory("ä"), s, flags=re.IGNORECASE)
    s = re.sub(rf"(?<![{vowel_class}])oe", repl_factory("ö"), s, flags=re.IGNORECASE)
    s = re.sub(rf"(?<![{vowel_class}])ue", repl_factory("ü"), s, flags=re.IGNORECASE)

    # Replace sss → ß (ASCII fallback for Eszett)
    s = re.sub(r"sss", "ß", s)
    s = re.sub(r"SSS", "ẞ", s)

    return s


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
        feedback.append(case_info)
        feedback.append(decl_info)
        return "\n".join(feedback)
