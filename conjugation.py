# conjugation.py

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
