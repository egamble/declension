
# ------------------
# articles.py
# ------------------

# -------------------------------
# Definite & Indefinite Articles
# -------------------------------

definite = {
    "masc": {"nom": "der", "acc": "den", "dat": "dem", "gen": "des"},
    "fem": {"nom": "die", "acc": "die", "dat": "der", "gen": "der"},
    "neut": {"nom": "das", "acc": "das", "dat": "dem", "gen": "des"},
    "plur": {"nom": "die", "acc": "die", "dat": "den", "gen": "der"},
}

indefinite = {
    "masc": {"nom": "ein", "acc": "einen", "dat": "einem", "gen": "eines"},
    "fem": {"nom": "eine", "acc": "eine", "dat": "einer", "gen": "einer"},
    "neut": {"nom": "ein", "acc": "ein", "dat": "einem", "gen": "eines"},
}

# -------------------------------
# Adjective Endings
# -------------------------------

weak = {
    ("masc", "nom"): "e", ("fem", "nom"): "e", ("neut", "nom"): "e", ("plur", "nom"): "en",
    ("masc", "acc"): "en", ("fem", "acc"): "e", ("neut", "acc"): "e", ("plur", "acc"): "en",
    ("masc", "dat"): "en", ("fem", "dat"): "en", ("neut", "dat"): "en", ("plur", "dat"): "en",
    ("masc", "gen"): "en", ("fem", "gen"): "en", ("neut", "gen"): "en", ("plur", "gen"): "en",
}

strong = {
    ("masc", "nom"): "er", ("fem", "nom"): "e", ("neut", "nom"): "es", ("plur", "nom"): "e",
    ("masc", "acc"): "en", ("fem", "acc"): "e", ("neut", "acc"): "es", ("plur", "acc"): "e",
    ("masc", "dat"): "em", ("fem", "dat"): "er", ("neut", "dat"): "em", ("plur", "dat"): "en",
    ("masc", "gen"): "en", ("fem", "gen"): "er", ("neut", "gen"): "en", ("plur", "gen"): "er",
}

mixed = {
    ("masc", "nom"): "er", ("neut", "nom"): "es", ("neut", "acc"): "es",
    ("masc", "dat"): "en", ("fem", "dat"): "en", ("neut", "dat"): "en",
    ("masc", "gen"): "en", ("fem", "gen"): "en", ("neut", "gen"): "en", ("plur", "gen"): "en",
}

def mixed_ending(gender, case):
    """Return the adjective ending for mixed declension (indefinite articles)."""
    return mixed.get((gender, case), weak.get((gender, case)))
