
# ------------------
# articles.py
# ------------------

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
