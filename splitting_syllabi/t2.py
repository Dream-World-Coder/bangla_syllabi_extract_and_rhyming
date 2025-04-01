import re

bangla_vowels:set[tuple[str, str]] = {
    ("অ", ""),
    ("আ", "া"),
    ("ই", "ি"),
    ("ঈ", "ী"),
    ("উ", "ু"),
    ("ঊ", "ূ"),
    ("ঋ", "ৃ"),
    ("এ", "ে"),
    ("ঐ", "ৈ"),
    ("ও", "ো"),
    ("ঔ", "ৌ")
}

bangla_consonants:set[str] = {
    "ক", "খ", "গ", "ঘ", "ঙ",
    "চ", "ছ", "জ", "ঝ", "ঞ",
    "ট", "ঠ", "ড", "ঢ", "ণ",
    "ত", "থ", "দ", "ধ", "ন",
    "প", "ফ", "ব", "ভ", "ম",
    "য", "র", "ল", "শ", "ষ", "স", "হ",
    "ড়", "ঢ়", "য়"
}

bangla_vowels_flattened: set[str] = {char for tup in bangla_vowels for char in tup}

def is_bangla_vowel(ch:str) -> bool:
    return ch in bangla_vowels_flattened

def is_bangla_consonant(ch:str) -> bool:
    return ch in bangla_consonants

def add_hosonto(seq: str) -> str:
    """
    Converts the last character of a given sequence to its 'Hosonto' form (adds Virama)
    if it is a Bangla consonant. If the last character is not in the Bangla Unicode block,
    the original sequence is returned unchanged.

    :param seq: A string sequence.
    :return: The modified sequence with the last character replaced by its Hosonto form,
             or the original sequence if the last character is not a Bangla consonant.
    """
    # If the sequence is empty, return it as is.
    if not seq:
        return seq

    # Get the last character of the sequence.
    last_char = seq[-1]

    # Check if the last character is a Bangla consonant.
    # if "\u0995" <= last_char <= "\u09DF":
    if is_bangla_consonant(last_char):
        # Replace the last character with the character followed by the Virama (Hosonto)
        return seq[:-1] + last_char + "\u09CD"

    # If it is not a Bangla consonant, return the original sequence unchanged.
    return seq

def replace_vowel_symbols_with_letters(seq: str) -> str:
    # a mapping dictionary from symbol to letter
    symbol_to_letter = {symbol: letter for letter, symbol in bangla_vowels if symbol}

    if not seq:
        return seq

    # process char by char
    result = ""
    for char in seq:
        # if character is a symbol, replace it with corresponding letter
        if char in symbol_to_letter:
            result += symbol_to_letter[char]
        else:
            # keep non-symbol characters as they are
            result += char

    return result

def is_swaranto(cd: str) -> bool:
    """Check if the string ends with a vowel (স্বরান্ত)."""
    return cd and is_bangla_vowel(cd[-1]) or False

def is_banjonanto(cd: str) -> bool:
    """Check if the string ends with a consonant (ব্যঞ্জনান্ত)."""
    return cd and is_bangla_consonant(cd[-1]) or False


def split_word_into_syllabi(word: str) -> list[str]:
    """
        * C-1: if ch[0] in bangla-vowels, then then split it and add in the syllabi tuple
        * C-2: find the CCV CVC CV VC patterns using the arrays, properly check
        * no-need for now: C-3: conjunct split :- if C-1 & C-2 if not followed then only split the word
    """
    word = word.strip()
    generated_syllabi: list[str] = []

    if not word:
        return ['']

    # Case 1:
    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        # if the word starts with a vowel, split it off
        # if it starts with a consonanat then split & add hosonto

    # 1.1 | eg আকাশ: ['আ', 'কাশ্']
    if len(word)!=1 and is_bangla_vowel(word[0]):
        generated_syllabi.append(word[0])
        word = word[1:]
    # 1.1x | eg ী: ['ঈ']
    elif len(word)==1 and is_bangla_vowel(word[0]):
        generated_syllabi.append(replace_vowel_symbols_with_letters(word[0]))
        word = word[1:]

    # 1.2 | eg ক: ['ক্'] -> handled later
    # elif len(word)==1 and is_bangla_consonant(word[0]):
    #     generated_syllabi.append(add_hosonto(word[0]))
    #     word = word[1:]

    # 1.3 | eg বিধাতার: ['বি', 'ধা', 'তা', 'র্']
    # elif len(word)>=2 and is_bangla_consonant(word[0]) and is_bangla_vowel(word[1]):
    #     generated_syllabi.append(word[:2])
    #     word = word[2:]



    # Case 2: Split based on cvc, ccv, cv, vc patterns
    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    is_matched:int = 0

    c = f'[{"".join(bangla_consonants)}]'
    v = f'[{"".join(bangla_vowels_flattened)}]'
    pattern = f'{c}{v}{c}|{c}{{2}}{v}|{c}{v}|{v}{c}'  # cvc | ccv | cv | vc

    matches = re.finditer(pattern, word)
    last_end = 0

    for match in matches:
        start, end = match.span()
        if start > last_end:
            # any unmatched portion __before__ the match
            generated_syllabi.append(add_hosonto(replace_vowel_symbols_with_letters(word[last_end:start])))
        generated_syllabi.append(add_hosonto(match.group())) # matched syllabi pattern
        last_end = end
        is_matched = 1

    # c* [ccc...] case ~~~ 1.2 case also handled here
    if is_matched==0 and len(word)>0:
        generated_syllabi.append(add_hosonto(word[0]))
        word = word[1:]
        # or
        # last_end = 1

    # any remaining part of the word, __after__ match
    if last_end < len(word):
        generated_syllabi.append(add_hosonto(replace_vowel_symbols_with_letters(word[last_end:])))

    return generated_syllabi







# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Test
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++
bangla_words:list[str] = [
    # very basic
    # "ঈ", "ী", "ক", "খ", "গ",

    # case 1
    "তুমি", "আকাশ", "কলম",

    # complex case 1
    "চলো", "বাংলা", "মানুষ",

    # case 2
    "মা",
    "দোলনা",
    "পরিবার",
    "বন্ধু",

    "বিদ্যালয়",
    "বিশ্ববিদ্যালয়",
    "রবীন্দ্রনাথ",
    "বিধাতার",
    "আনারস",

    # "চাট", "গড়", "হাট", "কাট", "লব", "ডাক", "টান", "নাম", "বল", "ধন",
    # "কলম", "সরম", "ঘরছ", "বসত", "নগর", "পলন", "মরক", "ভরত", "দরদ", "জলধ"
]
for word in bangla_words:
    print(f"{word}: {split_word_into_syllabi(word)}")

# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++
