import re

# juktakhor handling - not so proper, sometimes they themselves split & sometimes they stick together, can be optimised

class SplitBanglaSyllables:
    def __init__(self):
        self.bangla_vowels: set[tuple[str, str]] = {
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

        self.bangla_consonants: set[str] = {
            "ক", "খ", "গ", "ঘ", "ঙ",
            "চ", "ছ", "জ", "ঝ", "ঞ",
            "ট", "ঠ", "ড", "ঢ", "ণ",
            "ত", "থ", "দ", "ধ", "ন",
            "প", "ফ", "ব", "ভ", "ম",
            "য", "র", "ল", "শ", "ষ",
            "স", "হ", "ড়", "ঢ়", "য়",
        }

        self.bangla_vowels_flattened: set[str] = {char for tup in self.bangla_vowels for char in tup}

    def is_bangla_vowel(self, ch:str) -> bool:
        return ch in self.bangla_vowels_flattened

    def is_bangla_consonant(self, ch:str) -> bool:
        return ch in self.bangla_consonants

    def add_hosonto(self, seq: str) -> str:
        """
        Converts the last character of a given sequence to its 'hosonto' form (adds Virama)
        if it is a Bangla consonant. If the last character is not in the Bangla Unicode block,
        the original sequence is returned unchanged.

        :param seq: A string sequence.
        :return: The modified sequence with the last character replaced by its Hosonto form,
                or the original sequence if the last character is not a Bangla consonant.
        """
        if not seq:
            return seq

        last_char = seq[-1]

        # Check if the last character is a bangla consonant.
        # if "\u0995" <= last_char <= "\u09DF":
        if self.is_bangla_consonant(last_char):
            # Replace the last character with the character followed by the `virama` (hosonto)
            return seq[:-1] + last_char + "\u09CD"

        # If it is not a Bangla consonant, return the original sequence unchanged.
        return seq

    def replace_vowel_symbols_with_letters(self, seq: str) -> str:
        """("অ", ""),
        ("আ", "া") conversion"""
        # a mapping dictionary from symbol to letter
        symbol_to_letter = {symbol: letter for letter, symbol in self.bangla_vowels if symbol}

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

    def is_swaranto(self, seq: str) -> bool: # মুক্তদল
        """check if the string ends with a vowel (স্বরান্ত)."""
        return (seq and self.is_bangla_vowel(seq[-1])) or False

    def is_banjonanto(self, seq: str) -> bool:  # রুদ্ধদল
        """check if the string ends with a consonant (ব্যঞ্জনান্ত)."""
        if not seq:
            return False
        if seq[-1] == "\u09CD":  # hosonto (্)
            return True
        return self.is_bangla_consonant(seq[-1])

    def get_matra(self, generated_syllables, chhondo) -> int:
        """calculate matra of a word"""
        sum = 0
        for index, syllable in enumerate(generated_syllables):
            if self.is_swaranto(syllable): # always মাত্রা 1 for মুক্তদল
                sum += 1
            elif self.is_banjonanto(syllable):
                if chhondo == "স্বরবৃত্ত":
                    sum += 1 # both মুক্তদল এবং রুদ্ধদল: মাত্রা 1
                elif chhondo == "মাত্রাবৃত্ত":
                    sum += 2
                elif chhondo == "অক্ষরবৃত্ত":
                    if len(generated_syllables) == 1 or index == len(generated_syllables)-1: # একক ভাবে থাকলে অথবা শব্দান্তে থাকলে মাত্রা ২
                        sum += 2
                    else: # নাহলে মাত্রা ১
                        sum += 1
        return sum

    def split_word_into_syllables(self, word: str) -> tuple[str, list[str]]:
        """
            * C-1: if ch[0] in bangla-vowels, then then split it and add in the syllables tuple
            * C-2: find the CCV CVC CV VC patterns using the arrays, properly check
            * no-need for now: C-3: conjunct split :- if C-1 & C-2 if not followed then only split the word
        """
        word = word.strip()
        initial_word = word
        generated_syllables: list[str] = []

        if not word:
            return initial_word, generated_syllables

        # Case 1:
        # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++
            # if the word starts with a vowel, split it off
            # if it starts with a consonanat then split & add hosonto

        # 1.1 | eg আকাশ: ['আ', 'কাশ্']
        if len(word)!=1 and self.is_bangla_vowel(word[0]):
            generated_syllables.append(word[0])
            word = word[1:]
        # 1.1x | eg ী: ['ঈ']
        elif len(word)==1 and self.is_bangla_vowel(word[0]):
            generated_syllables.append(self.replace_vowel_symbols_with_letters(word[0]))
            word = word[1:]

        # 1.2 | eg ক: ['ক্'] -> handled later
        # elif len(word)==1 and is_bangla_consonant(word[0]):
        #     generated_syllables.append(add_hosonto(word[0]))
        #     word = word[1:]

        # 1.3 | eg বিধাতার: ['বি', 'ধা', 'তা', 'র্']
        # elif len(word)>=2 and is_bangla_consonant(word[0]) and is_bangla_vowel(word[1]):
        #     generated_syllables.append(word[:2])
        #     word = word[2:]



        # Case 2: Split based on cvc, ccv, cv, vc patterns
        # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        is_matched:bool = False

        c = f'[{"".join(self.bangla_consonants)}]'
        v = f'[{"".join(self.bangla_vowels_flattened)}]'
        pattern = f'{c}{v}{c}|{c}{{2}}{v}|{c}{v}|{v}{c}'  # cvc | ccv | cv | vc

        matches = re.finditer(pattern, word)
        last_end = 0

        for match in matches:
            start, end = match.span()
            if start > last_end:
                # any unmatched portion __before__ the match
                generated_syllables.append(self.add_hosonto(self.replace_vowel_symbols_with_letters(word[last_end:start])))
            generated_syllables.append(self.add_hosonto(match.group())) # matched syllables pattern
            last_end = end
            is_matched = True

        # ~~~~~~~~ case for cc
        if not is_matched and len(word)==2:
            generated_syllables.append(self.add_hosonto(word))
            last_end = 2

        # c* [ccc...], !cc || case ~~~ 1.2 case also handled here
        elif not is_matched and len(word)>0 and len(word)!=2:
            generated_syllables.append(self.add_hosonto(word[0]))
            word = word[1:]
            # or
            # last_end = 1

        # any remaining part of the word, __after__ match
        if last_end < len(word):
            generated_syllables.append(self.add_hosonto(self.replace_vowel_symbols_with_letters(word[last_end:])))

        return initial_word, generated_syllables

    def split_sentence_into_syllables(self, sentence: str) -> list[tuple[str, list[str]]]:
        sentence = sentence.strip()
        if not sentence:
            return []

        sentence = re.sub(r'[,.।;:]', '', sentence) # remove puntuations and spaces
        words:list = [word for word in sentence.split() if word]
        generated_syllables:list = [self.split_word_into_syllables(word) for word in words]

        return generated_syllables

    # def get_parts_of_speech(self, word:str) -> str:
    #     bnlp_pos = BengaliPOS()
    #     print(bnlp_pos.tag(word))
    #     return ""

    def __repr__(self):
        return "<SplitBanglaSyllables> Split Bangla words & sentences into syllables"


# check matra of অতিশয়" -- exception,


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Test
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++

if __name__ == "__main__":
    bangla_words:list[str] = [
        # very basic
        "ঈ", "ী", "ক", "খ", "গ",

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

        "চাট", "গড়", "হাট", "কাট", "লব", "ডাক", "টান", "নাম", "বল", "ধন",
        "কলম", "সরম", "ঘরছ", "বসত", "নগর", "পলন", "মরক", "ভরত", "দরদ", "জলধ"
    ]

    poem:str = """হাজার বছর ধরে আমি পথ হাঁটিতেছি পৃথিবীর পথে,
                সিংহল সমুদ্র থেকে নিশীথের অন্ধকারে মালয় সাগরে
                অনেক ঘুরেছি আমি; বিম্বিসার অশোকের ধূসর জগতে
                সেখানে ছিলাম আমি; আরো দূর অন্ধকারে বিদর্ভ নগরে;
                আমি ক্লান্ত প্রাণ এক, চারিদিকে জীবনের সমুদ্র সফেন,
                আমারে দুদণ্ড শান্তি দিয়েছিলো নাটোরের বনলতা সেন।

                চুল তার কবেকার অন্ধকার বিদিশার নিশা,
                মুখ তার শ্রাবস্তীর কারুকার্য; অতিদূর সমুদ্রের 'পর
                হাল ভেঙে যে নাবিক হারায়েছে দিশা
                সবুজ ঘাসের দেশ যখন সে চোখে দেখে দারুচিনি-দ্বীপের ভিতর,
                তেমনি দেখেছি তারে অন্ধকারে; বলেছে সে, 'এতোদিন কোথায় ছিলেন?'
                পাখির নীড়ের মত চোখ তুলে নাটোরের বনলতা সেন।

                সমস্ত দিনের শেষে শিশিরের শব্দের মতন
                সন্ধ্যা আসে; ডানার রৌদ্রের গন্ধ মুছে ফেলে চিল;
                পৃথিবীর সব রঙ নিভে গেলে পাণ্ডুলিপি করে আয়োজন
                তখন গল্পের তরে জোনাকির রঙে ঝিলমিল;
                সব পাখি ঘরে আসে—সব নদী—ফুরায় এ-জীবনের সব লেনদেন;
                থাকে শুধু অন্ধকার, মুখোমুখি বসিবার বনলতা সেন।"""

    splitter:SplitBanglaSyllables = SplitBanglaSyllables()

    file = "output.txt"

    # with open(file, "w") as f:
    #     for word in bangla_words:
    #         word, syllables = splitter.split_word_into_syllables(word)
    #         f.write(f"{word}: {syllables}\n")

    #     f.write("\n\nPOEM\n\n")
    #     syllables = splitter.split_sentence_into_syllables(poem)
    #     for item in syllables:
    #         f.write(f"{item[0]}: {item[1]}\n")

    syllables = splitter.split_word_into_syllables("অতিশয়")
    for chhondo in ["স্বরবৃত্ত", "মাত্রাবৃত্ত", "অক্ষরবৃত্ত"]:
        print(splitter.get_matra(syllables[1], chhondo))

    print("####")
    # +++++++++++++++++++++++++++++++++
    # They are different unicode char
    # +++++++++++++++++++++++++++++++++
    ch = 'য়'
    ch = 'য়'
    print(f'{splitter.is_swaranto(ch)=} {splitter.is_banjonanto(ch)=}')

# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++
'''
syllables=('অতিশয়', ['অ', 'তিশ্', 'য়'])
syllable='অ'
syllable='অ' is swaranto
syllable='তিশ্'
syllable='তিশ্' is banjonanto
syllable='য়'
2
syllable='অ'
syllable='অ' is swaranto
syllable='তিশ্'
syllable='তিশ্' is banjonanto
syllable='য়'
3
syllable='অ'
syllable='অ' is swaranto
syllable='তিশ্'
syllable='তিশ্' is banjonanto
syllable='য়'
2
'''
