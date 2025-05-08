import re

# bangla vowels and consonants
VOWELS = "অআইঈউঊঋএঐওঔািীুূৃেৈোৌ"
CONSONANTS = "কখগঘঙচছজঝঞটঠডঢণতথদধনপফবভমযরলশষসহ"
SPECIAL_CONSONANTS = "ংঃঁ"  # Nasal and visarga sounds
CONJUNCTS = ["ক্ত", "গ্ন", "শ্চ", "ঞ্জ", "ষ্ণ", "ষ্প", "ষ্ক", "ষ্ঠ", "ষ্ট"]  # Common conjuncts

def is_vowel(char):
    return char in VOWELS

def is_consonant(char):
    return char in CONSONANTS

def syllabify_bangla(word):
    """ Splits a Bengali word into syllables following linguistic rules """
    syllables = []
    i = 0
    while i < len(word):
        if is_vowel(word[i]):  # Start a new syllable with a vowel
            syllables.append(word[i])
            i += 1
        elif is_consonant(word[i]):  # Handle consonants
            if i + 1 < len(word) and is_vowel(word[i + 1]):
                # Consonant followed by vowel → Same syllable
                syllables.append(word[i] + word[i + 1])
                i += 2
            elif i + 1 < len(word) and word[i + 1] in SPECIAL_CONSONANTS:
                # Handle nasal sounds like "ং" and visarga "ঃ"
                syllables.append(word[i] + word[i + 1])
                i += 2
            elif i + 1 < len(word) and word[i + 1] in CONSONANTS:
                # Possible conjuncts
                if word[i:i+2] in CONJUNCTS:
                    syllables.append(word[i:i+2])  # Keep conjunct together
                    i += 2
                else:
                    # Break between two consonants
                    syllables.append(word[i])
                    i += 1
            else:
                syllables.append(word[i])
                i += 1
        else:
            # Catch-all for unknown characters
            syllables.append(word[i])
            i += 1

    return "-".join(syllables)

def process_bangla_sentence(sentence):
    """ Tokenizes and syllabifies an entire Bengali sentence """
    words = re.findall(r'[\u0980-\u09FF]+', sentence)  # Extract Bangla words
    return " | ".join(syllabify_bangla(word) for word in words)

# Example Usage
sentence = """হাজার বছর ধরে আমি পথ হাঁটিতেছি পৃথিবীর পথে,
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
print(process_bangla_sentence(sentence))





def get_hosonto(ch:str) -> str:
    match ch:
        case 'ক': return 'ক্'
        case 'খ': return 'খ্'
        case 'গ': return 'গ্'
        case 'ঘ': return 'ঘ্'
        case 'ঙ': return 'ঙ্'
        case 'চ': return 'চ্'
        case 'ছ': return 'ছ্'
        case 'জ': return 'জ্'
        case 'ঝ': return 'ঝ্'
        case 'ঞ': return 'ঞ্'
        case 'ট': return 'ট্'
        case 'ঠ': return 'ঠ্'
        case 'ড': return 'ড্'
        case 'ঢ': return 'ঢ্'
        case 'ণ': return 'ণ্'
        case 'ত': return 'ত্'
        case 'থ': return 'থ্'
        case 'দ': return 'দ্'
        case 'ধ': return 'ধ্'
        case 'ন': return 'ন্'
        case 'প': return 'প্'
        case 'ফ': return 'ফ্'
        case 'ব': return 'ব্'
        case 'ভ': return 'ভ্'
        case 'ম': return 'ম্'
        case 'য': return 'য্'
        case 'র': return 'র্'
        case 'ল': return 'ল্'
        case 'শ': return 'শ্'
        case 'ষ': return 'ষ্'
        case 'স': return 'স্'
        case 'হ': return 'হ্'
        case 'ড়': return 'ড়্'
        case 'ঢ়': return 'ঢ়্'
        case 'য়': return 'য়্'
        case _: return ch  # return the character unchanged if it's not a consonant
