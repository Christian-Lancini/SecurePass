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
    "'": '', '<': '{', '>': '}', '[': '<', ']': '>',
    '(': '~', ')': '=', '&': '&',  

    # spazi e ritorno a capo
    '\n': '\n', ' ': '~',

    # tabulazione
    '\t': '|',
}


def cifra_stringa(stringa):
    """Cripta una stringa usando il dizionario di sostituzione"""
    return ''.join(sostituzione.get(c, c) for c in stringa)

def backup_crypt():
    path = "password/backup_try.txt"

    with open(path, "r") as f:
        contenuto = f.read()

    # Cripta l'intero contenuto come singola stringa
    criptato = cifra_stringa(contenuto)

    with open(path, "w") as f:
        f.write(criptato)

    print("File criptato con successo.")
