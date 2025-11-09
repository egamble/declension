
# ------------------
# sentence.py
# ------------------

import random
from vocabulary import nouns, adjectives, verbs, subjects, dat_prepositions, acc_prepositions, gen_prepositions
from articles import definite, indefinite, weak, strong, mixed, mixed_ending
from conjugation import conjugate_en, conjugate_de

# ------------------------------------------------------------
# Noun declension helper
# ------------------------------------------------------------

# Weak masculine nouns that add -en or -n in oblique cases (acc/dat)
weak_nouns = {
    "Mensch": "Menschen",
    "Junge": "Jungen",
    "Student": "Studenten",
    "Herr": "Herren",
    "Nachbar": "Nachbarn",
    "Kollege": "Kollegen",
    "Polizist": "Polizisten",
    "Präsident": "Präsidenten",
    "Name": "Namen"
}

def decline_noun(noun, gender, case, number):
    """
    Returns the correctly declined form of a German noun
    (handles weak masculine nouns, plural datives, and genitive endings).
    """
    # Weak masculine nouns in singular (Acc/Dat/Gen)
    if gender == "masc" and number == "sing" and case in ("acc", "dat", "gen"):
        if noun in weak_nouns:
            return weak_nouns[noun]

    # Genitive singular masculine/neuter adds -s or -es
    if number == "sing" and case == "gen" and gender in ("masc", "neut"):
        if noun.endswith(("s", "ß", "x", "z", "tz", "sch")):
            noun = noun + "es"
        else:
            noun = noun + "s"

    # Plural dative nouns add -n if not ending in -n or -s
    if number == "plur" and case == "dat":
        if not noun.endswith(("n", "s")):
            noun = noun + "n"

    return noun

def cap_first(s: str) -> str:
    """Uppercase the first character only, leave the rest unchanged."""
    return s[:1].upper() + s[1:] if s else s

def generate_sentence():
    # Randomly choose sentence type: preposition or verb
    use_preposition = random.choice([True, False])

    subj_en, subj_de = random.choice(subjects)
    verb_en, verb_de, verb_case, *extras = random.choice(verbs)
    noun, gender, en_sing, en_plur, de_plur = random.choice(nouns)
    adj_de, adj_en = random.choice(adjectives)
    det_type = random.choice(["definite", "indefinite", "no_article"])
    plural = random.choice([True, False])
    number = "plur" if plural else "sing"

    # Select case
    if use_preposition:
        prep_type = random.choice(["acc", "dat", "gen"])
        if prep_type == "acc":
            prep_de, prep_en = random.choice(acc_prepositions)
            case = "acc"
        elif prep_type == "dat":
            prep_de, prep_en = random.choice(dat_prepositions)
            case = "dat"
        else:
            prep_de, prep_en = random.choice(gen_prepositions)
            case = "gen"
    else:
        if verb_case in ("nom", "acc", "dat", "gen"):
            case = verb_case
        else:
            case = "nom"
            
    noun_de = decline_noun(de_plur if plural else noun, gender, case, number)
    obj_en = en_plur if plural else en_sing

    # Determine German article & declension type
    if det_type == "definite":
        article_de = definite[gender if number == "sing" else "plur"][case]
        ending = weak[(gender if number == "sing" else "plur", case)]
        decl_type = "weak"
    elif det_type == "indefinite" and number == "sing":
        article_de = indefinite[gender][case]
        ending = mixed_ending(gender, case)
        decl_type = "mixed"
    elif det_type == "no_article":
        article_de = ""
        ending = strong[(gender if number == "sing" else "plur", case)]
        decl_type = "strong"
    else:
        article_de = ""
        ending = strong[("plur", case)]
        decl_type = "strong"

    adj_full = adj_de + ending

    # Build German noun phrase
    np_parts = [article_de, adj_full, noun_de]
    np_de = " ".join(p for p in np_parts if p)

    # English article matching German
    if article_de:
        if det_type == "definite":
            art_en = "the"
        elif det_type == "indefinite" and number == "sing":
            art_en = "a"
        else:
            art_en = ""
    else:
        art_en = ""

    # English NP
    if art_en:
        obj_en_phrase = f"{art_en} {adj_en} {obj_en}"
    else:
        obj_en_phrase = f"{adj_en} {obj_en}"

    # Build sentences
    if use_preposition:
        np_de = prep_de + " " + np_de if prep_de else np_de
        if art_en:
            np_en = f"{prep_en} {art_en} {adj_en} {obj_en}".strip()
        else:
            np_en = f"{prep_en} {adj_en} {obj_en}".strip()
        sentence_en = np_en.capitalize() + "."
        german_sentence = cap_first(np_de) + "."
    else:
        verb_form_en = conjugate_en(verb_en, subj_en)
        verb_form_de = conjugate_de(verb_de, subj_de, subj_en)
        sentence_en = f"{subj_en.capitalize()} {verb_form_en} {obj_en_phrase}."
        german_sentence = f"{subj_de.capitalize()} {verb_form_de} {np_de}."

    return {
        "english": sentence_en,
        "german_correct": german_sentence,
        "meta": {
            "article": article_de,
            "adj": adj_de,
            "adj_full": adj_full,
            "noun_de": noun_de,
            "case": case,
            "declension_type": decl_type
        }
    }
