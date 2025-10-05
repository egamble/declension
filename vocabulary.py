# vocabulary.py

# Subjects (EN, DE)

# ------------------
# vocabulary.py
# ------------------

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
    ("Blume", "fem", "flower", "flowers", "Blumen"),

    # Weak masculine nouns (decline in acc/dat)
    ("Junge", "masc", "boy", "boys", "Jungen"),
    ("Student", "masc", "student", "students", "Studenten"),
    ("Herr", "masc", "gentleman", "gentlemen", "Herren"),
    ("Mensch", "masc", "person", "people", "Menschen"),
    ("Name", "masc", "name", "names", "Namen"),
    ("Polizist", "masc", "policeman", "policemen", "Polizisten"),
    ("Präsident", "masc", "president", "presidents", "Präsidenten"),
    ("Kollege", "masc", "colleague", "colleagues", "Kollegen"),
    ("Nachbar", "masc", "neighbor", "neighbors", "Nachbarn")
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
