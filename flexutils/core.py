import unicodedata
import string

# --- THE NORMALIZE ENGINE ---

def normalize(text):
    """
    Strips whitespace, lowers case, removes punctuation, and strips accents.
    Converts '  Résumé! ' into 'resume'.
    """
    if text is None:
        return ""
    
    # 1. Convert to string, lowercase, and strip trailing spaces
    txt = str(text).strip().casefold()
    
    # 2. Remove accents (normalize unicode characters)
    txt = "".join(
        c for c in unicodedata.normalize('NFD', txt)
        if unicodedata.category(c) != 'Mn'
    )
    
    # 3. Strip out all punctuation
    txt = txt.translate(str.maketrans('', '', string.punctuation))
    
    return txt


# --- 1. SENSITIVITY-FREE COMPARISONS ---

def matches(str1, str2):
    """True if strings are identical after ignoring case, spaces, accents, and punctuation."""
    return normalize(str1) == normalize(str2)

def contains(main_str, sub_str):
    """True if substring exists inside main string, ignoring all formatting barriers."""
    return normalize(sub_str) in normalize(main_str)


# --- 2. THE BULLETPROOF DICTIONARY ---

class FlexDict(dict):
    """
    A dictionary that ignores case, spacing, accents, and punctuation in keys.
    Also returns None instead of crashing if a key doesn't exist.
    """
    def __setitem__(self, key, value):
        super().__setitem__(normalize(key), value)

    def __getitem__(self, key):
        return super().get(normalize(key), None)

    def __contains__(self, key):
        return super().__contains__(normalize(key))

    def get(self, key, default=None):
        return super().get(normalize(key), default)


# --- 3. REPETITIVE FILE SHORTCUTS ---

def read_txt(file_path):
    """Reads a text file safely without crashing if the file doesn't exist."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return ""

def write_txt(file_path, content):
    """Instantly writes content to a file, making sure it converts to string."""
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(str(content))