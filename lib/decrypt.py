import json

# Dizionario di sostituzione (stesso dell'encryption)
sostituzione = {
    'a': 'q', 'b': 'w', 'c': 'e', 'd': 'r',
    'e': 't', 'f': 'y', 'g': 'u', 'h': 'i',
    'i': 'o', 'j': 'p', 'k': 'a', 'l': 's',
    'm': 'd', 'n': 'f', 'o': 'g', 'p': 'h',
    'q': 'j', 'r': 'k', 's': 'l', 't': 'z',
    'u': 'x', 'v': 'c', 'w': 'v', 'x': 'b',
    'y': 'n', 'z': 'm',

    'A': 'Q', 'B': 'W', 'C': 'E', 'D': 'R',
    'E': 'T', 'F': 'Y', 'G': 'U', 'H': 'I',
    'I': 'O', 'J': 'P', 'K': 'A', 'L': 'S',
    'M': 'D', 'N': 'F', 'O': 'G', 'P': 'H',
    'Q': 'J', 'R': 'K', 'S': 'L', 'T': 'Z',
    'U': 'X', 'V': 'C', 'W': 'V', 'X': 'B',
    'Y': 'N', 'Z': 'M',

    '0': '!', '1': '@', '2': '#', '3': '$', '4': '%',
    '5': '^', '6': '&', '7': '*', '8': '(', '9': ')',

    ':': '-', '"': '+', '{': '[', '}': ']',
    ',': ';', '.': ':', '?': '/', '!': '_',
    "'": '`', '<': '{', '>': '}', '[': '<', ']': '>',
    '(': '~', ')': '=', '&': '&',  

    '\n': '\n', ' ': '~',
    '\t': '|',
}

# Inversione del dizionario
invertito = {v: k for k, v in sostituzione.items()}

def decifra_stringa(stringa):
    """Decifra una stringa usando il dizionario invertito"""
    return ''.join(invertito.get(c, c) for c in stringa)

def decrypt(file=None):  # parametro file è opzionale
    path = "password/password.json"

    # Leggi il file con le password cifrate
    with open(path, "r") as f:
        contenuto = json.load(f)

    # Decifra ogni password
    decifrate = [decifra_stringa(pw) for pw in contenuto]

    # Sovrascrivi il file con le password decifrate
    with open(path, "w") as f:
        json.dump(decifrate, f, indent=4)

    print("File decriptato con successo.")
