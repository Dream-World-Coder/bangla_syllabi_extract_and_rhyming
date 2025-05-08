import re

bangla_vowels: set[tuple[str, str]] = {
    ("অ", ""), ("আ", "া"), ("ই", "ি"), ("ঈ", "ী"), ("উ", "ু"),
    ("ঊ", "ূ"), ("ঋ", "ৃ"), ("এ", "ে"), ("ঐ", "ৈ"), ("ও", "ো"), ("ঔ", "ৌ")
}

bangla_consonants: set[str] = {
    "ক", "খ", "গ", "ঘ", "ঙ", "চ", "ছ", "জ", "ঝ", "ঞ",
    "ট", "ঠ", "ড", "ঢ", "ণ", "ত", "থ", "দ", "ধ", "ন",
    "প", "ফ", "ব", "ভ", "ম", "য", "র", "ল", "শ", "ষ", "স", "হ",
    "ড়", "ঢ়", "য়"
}

bangla_special_chars: set[str] = {"ং", "ঃ", "ঁ"}  # Anusvara, Visarga, Candrabindu

bangla_vowels_flattened: set[str] = {char for tup in bangla_vowels for char in tup if char}
bangla_independent_vowels: set[str] = {tup[0] for tup in bangla_vowels}
bangla_vowel_diacritics: set[str] = {tup[1] for tup in bangla_vowels if tup[1]}

def is_bangla_vowel(ch: str) -> bool:
    return ch in bangla_vowels_flattened

def is_bangla_consonant(ch: str) -> bool:
    return ch in bangla_consonants

def is_bangla_special(ch: str) -> bool:
    return ch in bangla_special_chars

def add_hosonto(seq: str) -> str:
    if not seq or not is_bangla_consonant(seq[-1]):
        return seq
    return seq + "\u09CD"  # Virama

def split_word_into_syllabi(word: str) -> list[str]:
    """
    Splits a Bangla word into syllables considering consonants, vowels, conjuncts, and special characters.
    - Independent vowels form standalone syllables.
    - Consonants with vowel diacritics or inherent vowels form syllables.
    - Conjuncts (C + Virama + C) are treated as single units.
    - Special characters (e.g., Anusvara) are attached to the previous syllable.
    - Hosonto is added to non-final syllables ending in consonants.
    """
    word = word.strip()
    if not word:
        return []

    syllabi = []
    i = 0
    inherent_vowel = "অ"  # Representing the inherent 'ô' sound

    while i < len(word):
        current_syllable = ""

        # Case 1: Independent vowel starts a syllable
        if is_bangla_vowel(word[i]) and word[i] in bangla_independent_vowels:
            current_syllable = word[i]
            i += 1

        # Case 2: Consonant (possibly part of a conjunct) starts a syllable
        elif is_bangla_consonant(word[i]):
            current_syllable = word[i]
            i += 1

            # Check for conjuncts (C + Virama + C)
            while i < len(word) - 1 and word[i] == "\u09CD" and is_bangla_consonant(word[i + 1]):
                current_syllable += "\u09CD" + word[i + 1]
                i += 2

            # Check for vowel diacritic following the consonant or conjunct
            if i < len(word) and word[i] in bangla_vowel_diacritics:
                current_syllable += word[i]
                i += 1
            # If no diacritic and not at word end, assume inherent vowel (except for final consonant)
            elif i < len(word):
                current_syllable += inherent_vowel

        # Case 3: Special character (attach to previous syllable if exists)
        elif is_bangla_special(word[i]):
            if syllabi:
                syllabi[-1] += word[i]
            else:
                current_syllable = word[i]
            i += 1

        # Append non-empty syllable
        if current_syllable:
            syllabi.append(current_syllable)

    # Post-processing: Add hosonto to non-final syllables ending with consonants
    for j in range(len(syllabi) - 1):
        if is_bangla_consonant(syllabi[j][-1]):
            syllabi[j] = add_hosonto(syllabi[j])

    return syllabi

# Test the function
bangla_words = ["না", "মা", "তুমি", "চলো", "বাংলা", "কলম", "বন্ধু", "আকাশ", "মানুষ",
                "পরিবার", "বিদ্যালয়", "বিশ্ববিদ্যালয়", "রবীন্দ্রনাথ", "দোলনা", "বিধাতার"]

for word in bangla_words:
    print(f"{word}: {split_word_into_syllabi(word)}")

'''
না: ['না']
মা: ['মা']
তুমি: ['তু', 'মি']
চলো: ['চঅ', 'লো']
বাংলা: ['বাং', 'লা']
কলম: ['কঅ', 'লঅ', 'ম']
বন্ধু: ['বঅ', 'ন্ধু']
আকাশ: ['আ', 'কা', 'শ']
মানুষ: ['মা', 'নু', 'ষ']
পরিবার: ['পঅ', 'রি', 'বা', 'র']
'''
