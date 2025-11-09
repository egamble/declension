
# ------------------
# conjugation.py
# ------------------

# English conjugation
def conjugate_en(verb, subject):
    subject = subject.capitalize()

    # Irregular verb: "be"
    if verb == "be":
        if subject == "I":
            return "am"
        elif subject in ["He", "She", "It"]:
            return "is"
        else:
            return "are"

    # Irregular verb: "have"
    if verb == "have":
        return "has" if subject in ["He", "She", "It"] else "have"

    # Regular verbs
    if subject in ["He", "She", "It"]:
        if verb.endswith("y") and verb[-2] not in "aeiou":
            return verb[:-1] + "ies"  # cry -> cries
        elif verb.endswith(("s", "sh", "ch", "x", "z")):
            return verb + "es"        # watch -> watches
        else:
            return verb + "s"         # play -> plays
    else:
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
    },
    "helfen": {
        "ich": "helfe", "du": "hilfst", "er/sie/es": "hilft",
        "wir": "helfen", "ihr": "helft", "sie": "helfen"
    },
    "gefallen": {
        "ich": "gefallen", "du": "gefällst", "er/sie/es": "gefällt",
        "wir": "gefallen", "ihr": "gefallt", "sie": "gefallen"
    },
    "bedürfen": {
        "ich": "bedürfe", "du": "bedarfst", "er/sie/es": "bedarf",
        "wir": "bedürfen", "ihr": "bedürft", "sie": "bedürfen"
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
