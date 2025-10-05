# ------------------------------------------------------------
# articles.py
# ------------------------------------------------------------

# -------------------------------
# Definite & Indefinite Articles
# -------------------------------

definite = {
    "masc": {"nom": "der", "acc": "den", "dat": "dem"},
    "fem": {"nom": "die", "acc": "die", "dat": "der"},
    "neut": {"nom": "das", "acc": "das", "dat": "dem"},
    "plur": {"nom": "die", "acc": "die", "dat": "den"},
}

indefinite = {
    "masc": {"nom": "ein", "acc": "einen", "dat": "einem"},
    "fem": {"nom": "eine", "acc": "eine", "dat": "einer"},
    "neut": {"nom": "ein", "acc": "ein", "dat": "einem"},
}

# -------------------------------
# Adjective Endings
# -------------------------------

weak = {
    ("masc", "nom"): "e", ("fem", "nom"): "e", ("neut", "nom"): "e", ("plur", "nom"): "en",
    ("masc", "acc"): "en", ("fem", "acc"): "e", ("neut", "acc"): "e", ("plur", "acc"): "en",
    ("masc", "dat"): "en", ("fem", "dat"): "en", ("neut", "dat"): "en", ("plur", "dat"): "en",
}

strong = {
    ("masc", "nom"): "er", ("fem", "nom"): "e", ("neut", "nom"): "es", ("plur", "nom"): "e",
    ("masc", "acc"): "en", ("fem", "acc"): "e", ("neut", "acc"): "es", ("plur", "acc"): "e",
    ("masc", "dat"): "em", ("fem", "dat"): "er", ("neut", "dat"): "em", ("plur", "dat"): "en",
}

mixed = {
    ("masc", "nom"): "er", ("neut", "nom"): "es", ("neut", "acc"): "es",
    ("masc", "dat"): "en", ("fem", "dat"): "en", ("neut", "dat"): "en",
}

def mixed_ending(gender, case):
    """Return the adjective ending for mixed declension (indefinite articles)."""
    return mixed.get((gender, case), weak.get((gender, case)))



# ------------------------------------------------------------
# conjugation.py
# ------------------------------------------------------------

# English conjugation
def conjugate_en(verb, subject):
    if subject in ["He", "She", "It"]:
        if verb.endswith("y") and verb[-2] not in "aeiou":
            return verb[:-1] + "ies"
        elif verb.endswith(("s", "sh", "ch", "x", "z")):
            return verb + "es"
        elif verb == "be":
            return "is"
        elif verb == "have":
            return "has"
        else:
            return verb + "s"
    elif subject == "I":
        if verb == "be":
            return "am"
        return verb
    elif subject in ["You", "We", "They"]:
        if verb == "be":
            return "are"
        return verb
    return verb

# German irregular verbs
irregular_de = {
    "sein": {
        "ich": "bin", "du": "bist", "er/sie/es": "ist",
        "wir": "sind", "ihr": "seid", "sie": "sind"
    },
    "haben": {
        "ich": "habe", "du": "hast", "er/sie/es": "hat",
        "wir": "haben", "ihr": "habt", "sie": "haben"
    },
    "essen": {
        "ich": "esse", "du": "isst", "er/sie/es": "isst",
        "wir": "essen", "ihr": "esst", "sie": "essen"
    },
    "sehen": {
        "ich": "sehe", "du": "siehst", "er/sie/es": "sieht",
        "wir": "sehen", "ihr": "seht", "sie": "sehen"
    },
    "mögen": {
        "ich": "mag", "du": "magst", "er/sie/es": "mag",
        "wir": "mögen", "ihr": "mögt", "sie": "mögen"
    }
}

def conjugate_de(verb, subj_de, subj_en):
    person = subj_en.lower()
    if verb in irregular_de:
        if person == "i":
            return irregular_de[verb]["ich"]
        elif person == "you":
            return irregular_de[verb]["du"]
        elif person in ["he", "she", "it"]:
            return irregular_de[verb]["er/sie/es"]
        elif person == "we":
            return irregular_de[verb]["wir"]
        elif person == "they":
            return irregular_de[verb]["sie"]

    stem = verb[:-2]  # drop -en
    endings = {
        "i": "e",
        "you": "st",
        "he": "t",
        "she": "t",
        "it": "t",
        "we": "en",
        "they": "en"
    }
    return stem + endings.get(person, "en")



# ------------------------------------------------------------
# diagnose.py
# ------------------------------------------------------------

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
    case_names = {"nom": "nominative", "acc": "accusative", "dat": "dative"}
    problems.append(f"(This noun phrase is in the **{case_names[meta['case']]}** case.)")
    problems.append(f"(Declension type: **{meta['declension_type']}**).")

    # Final evaluation
    if len(problems) <= 2 and normalize(user_in).lower() == normalize(correct).lower():
        return "✅ Correct!"
    else:
        feedback = ["❌ Not quite.", "Correct: " + correct]
        if problems:
            feedback.append("Details:")
            feedback.extend(" - " + p for p in problems)
        return "\n".join(feedback)



# ------------------------------------------------------------
# feedback.py
# ------------------------------------------------------------

# -*- coding: utf-8 -*-
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

    case_names={"nom":"nominative","acc":"accusative","dat":"dative"}
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



# ------------------------------------------------------------
# main.py
# ------------------------------------------------------------

from sentence import generate_sentence
from diagnose import diagnose

def main():
    print("=== German Declension Trainer ===")
    print("Type 'quit' or 'exit' to stop.\n")

    score = 0
    total = 0

    while True:
        data = generate_sentence()
        print("EN:", data["english"])

        try:
            from prompt_toolkit import prompt
            user = prompt("DE: ")
        except ImportError:
            user = input("DE: ")

        if user.lower() in ("quit", "exit"):
            print(f"Final score: {score}/{total}")
            break

        total += 1
        result = diagnose(user, data["german_correct"], data["meta"])
        if "✅" in result:
            score += 1

        print(result)
        print(f"Score: {score}/{total}\n")

if __name__ == "__main__":
    main()



# ------------------------------------------------------------
# sentence.py
# ------------------------------------------------------------

import random
from vocabulary import nouns, adjectives, verbs, subjects, dat_prepositions, acc_prepositions
from articles import definite, indefinite, weak, strong, mixed, mixed_ending
from conjugation import conjugate_en, conjugate_de

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
        if random.choice([True, False]):
            prep_de, prep_en = random.choice(dat_prepositions)
            case = "dat"
        else:
            prep_de, prep_en = random.choice(acc_prepositions)
            case = "acc"
    else:
        if verb_case == "nom":
            case = "nom"
        elif verb_case == "acc":
            case = "acc"
        else:
            # safety fallback
            case = "nom"

    noun_de = de_plur if plural else noun
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



# ------------------------------------------------------------
# vocabulary.py
# ------------------------------------------------------------

# Subjects (EN, DE)
subjects = [
    ("I", "ich"),
    ("you", "du"),
    ("he", "er"),
    ("she", "sie"),
    ("we", "wir"),
    ("they", "sie")
]

# Nouns: (German noun, gender, English singular, English plural, German plural)
nouns = [
    ("Mann", "masc", "man", "men", "Männer"),
    ("Frau", "fem", "woman", "women", "Frauen"),
    ("Kind", "neut", "child", "children", "Kinder"),
    ("Hund", "masc", "dog", "dogs", "Hunde"),
    ("Katze", "fem", "cat", "cats", "Katzen"),
    ("Haus", "neut", "house", "houses", "Häuser"),
    ("Auto", "neut", "car", "cars", "Autos"),
    ("Blume", "fem", "flower", "flowers", "Blumen")
]

# Adjectives: (German stem, English)
adjectives = [
    ("klein", "small"),
    ("groß", "big"),
    ("schön", "beautiful"),
    ("neu", "new"),
    ("alt", "old"),
    ("freundlich", "friendly"),
    ("rot", "red"),
    ("schnell", "fast")
]

# Verbs: (EN, DE, required case)
verbs = [
    ("see", "sehen", "acc"),
    ("have", "haben", "acc"),
    ("like", "mögen", "acc"),
    ("buy", "kaufen", "acc"),
    ("eat", "essen", "acc"),
    ("be", "sein", "nom"), # This is replicated to make nominative more likely.
    ("be", "sein", "nom"),
    ("be", "sein", "nom"),
]

# Dative prepositions: (DE, EN)
dat_prepositions = [
    ("mit", "with"),
    ("nach", "to/after"),
    ("bei", "at/near"),
    ("von", "from"),
    ("zu", "to"),
    ("aus", "out of"),
    ("seit", "since/for")
]

# Accusative prepositions: (DE, EN)
acc_prepositions = [
    ("für", "for"),
    ("durch", "through"),
    ("gegen", "against"),
    ("ohne", "without"),
    ("um", "around"),
    ("entlang", "along")
]
