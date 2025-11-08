import json

# Dizionario di sostituzione
sostituzione = {
    # lettere minuscole
    'a': 'q', 'b': 'w', 'c': 'e', 'd': 'r',
    'e': 't', 'f': 'y', 'g': 'u', 'h': 'i',
    'i': 'o', 'j': 'p', 'k': 'a', 'l': 's',
    'm': 'd', 'n': 'f', 'o': 'g', 'p': 'h',
    'q': 'j', 'r': 'k', 's': 'l', 't': 'z',
    'u': 'x', 'v': 'c', 'w': 'v', 'x': 'b',
    'y': 'n', 'z': 'm',

    # lettere maiuscole
    'A': 'Q', 'B': 'W', 'C': 'E', 'D': 'R',
    'E': 'T', 'F': 'Y', 'G': 'U', 'H': 'I',
    'I': 'O', 'J': 'P', 'K': 'A', 'L': 'S',
    'M': 'D', 'N': 'F', 'O': 'G', 'P': 'H',
    'Q': 'J', 'R': 'K', 'S': 'L', 'T': 'Z',
    'U': 'X', 'V': 'C', 'W': 'V', 'X': 'B',
    'Y': 'N', 'Z': 'M',

    # numeri
    '0': '!', '1': '@', '2': '#', '3': '$', '4': '%',
    '5': '^', '6': '&', '7': '*', '8': '(', '9': ')',

    # simboli di punteggiatura
    ':': '-', '"': '+', '{': '[', '}': ']',
    ',': ';', '.': ':', '?': '/', '!': '_',
    "'": '`', '<': '{', '>': '}', '[': '<', ']': '>',
    '(': '~', ')': '=', '&': '&',  

    # spazi e ritorno a capo
    '\n': '\n', ' ': '~',

    # tabulazione
    '\t': '|',
}


def cifra_stringa(stringa):
    """Cripta una stringa usando il dizionario di sostituzione"""
    return ''.join(sostituzione.get(c, c) for c in stringa)


def crypt():
    path = "password/password.json"

    with open(path, "r") as f:
        contenuto = json.load(f)

    # Cripta ogni password nella lista
    criptate = [cifra_stringa(pw) for pw in contenuto]

    with open(path, "w") as f:
        json.dump(criptate, f, indent=4)

    print("File criptato con successo.")
