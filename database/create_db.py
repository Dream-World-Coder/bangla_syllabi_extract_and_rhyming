''' // SCHEMA : table/document: 'words'

    {
        word,
        syllables:[],
        totalMatra:{
            স্বরবৃত্ত,
            মাত্রাবৃত্ত,
            অক্ষরবৃত্ত
        },
        POS : , poems do not follow specific s-v-o order
    }
'''

# from ..splitting_syllabi.splitBanglaSyllables import SplitBanglaSyllables
import json
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from word_to_syllables.splitBanglaSyllables import SplitBanglaSyllables

def create_word_database(read_file="passage.txt", write_file="db/words.json"):
    read_file = os.path.join(os.getcwd(), f'database/{read_file}')
    write_file = os.path.join(os.getcwd(), f'database/{write_file}')

    splitter = SplitBanglaSyllables()
    content = ""

    with open(read_file, "r", encoding="utf-8") as f:
        content = f.read()

    # split into syllables
    # syllables = []
    # for sentence in content.split("\n"):
    #     syllables.append(splitter.split_sentence_into_syllables(sentence))
    syllables = splitter.split_sentence_into_syllables(content)

    # building word entries
    word_entries = []
    for word, sylls in syllables:
        entry = {
            "word": word,
            "syllables": sylls,
            "totalMatra": {
                "স্বরবৃত্ত": splitter.get_matra(sylls, "স্বরবৃত্ত"),
                "মাত্রাবৃত্ত": splitter.get_matra(sylls, "মাত্রাবৃত্ত"),
                "অক্ষরবৃত্ত": splitter.get_matra(sylls, "অক্ষরবৃত্ত")
            },
            "POS": splitter.get_parts_of_speech(word)
        }
        word_entries.append(entry)

    # write to JSON
    with open(write_file, "w", encoding="utf-8") as f:
        json.dump({"words": word_entries}, f, ensure_ascii=False, indent=4)

    print(f"Word database written to {write_file}")


if __name__=="__main__":
    create_word_database()
