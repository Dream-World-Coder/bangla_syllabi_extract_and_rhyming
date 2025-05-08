import re
import json
import random

def determine_chhondo(pattern) -> tuple[str, list[int]]:
    """
    Here the chhondo is determined by highest matra, so if we set 2|2|2|8 it will be akhorbritto, and give strange results,
    thats why here input must be given in proper way like 4n+2, 5n+2 etc not 2n+8 because they are not usual poem structures
    """
    # validate pattern & determine ছন্দ from that
    # +++++++++++++++++++++++++++++++++++++++++++
    if not pattern:
        raise Exception("pattern not found")

    # check pattern structure <num>|<num>|...|<num>
    if not re.fullmatch(r'^(\d+\|)*\d+$', pattern): # ^ ... $ are not needed, for fullMatch
        raise Exception("Invalid pattern format. Use <num>|<num>|...|<num> (e.g., 4|4|4|2)")

    extracted_pattern = list(map(int, pattern.split('|')))

    chhondo = ""
    highest_matra = max(extracted_pattern)

    if highest_matra<2:
        raise Exception("matra should at least be 2")

    if 2 <= highest_matra <= 4:
        chhondo = "স্বরবৃত্ত"
    elif 5 <= highest_matra <= 7:
        chhondo = "মাত্রাবৃত্ত"
    elif 8 <= highest_matra <= 10+2: # acctually 10 but giving 2 extra for testing results, fix later
        chhondo = "অক্ষরবৃত্ত"
    else:
        # chhondo = "undefined"
        raise Exception("matra at max can be 10")

    return chhondo, extracted_pattern


def find_valid_words(words_list, chhondo, matra):
    return [word for word in words_list if word['totalMatra'][chhondo] == matra]

def generate_random_poem(db_path:str, pattern:str, no_of_lines_per_stanza:int=2, no_of_stanza:int=1):
    if not db_path: # validate db_path
        print("database path not found")
        return

    # get chhondo
    chhondo, extracted_pattern = determine_chhondo(pattern)

    # no_of_lines_per_stanza = 2 (fixed now) # later will expand to 2-8
    # no_of_stanza = any int
    if not isinstance(no_of_stanza, int) or not isinstance(no_of_lines_per_stanza, int):
        print("Invalid input: stanza count and lines per stanza must be integers")
        return

    no_of_lines_per_stanza = 2 # fixing to 2 for now
    no_of_stanza = min(no_of_stanza, 8) # max 8


    # loading words database
    # +++++++++++++++++++++++++
    words_data = None
    with open(db_path, 'r') as f:
        words_data = json.load(f)

    if not words_data or not words_data.get("words"):
        print("Unable to retrive json words data")
        return

    words_list = words_data.get("words")

    # creating poem
    # +++++++++++++++++
    stanza = []
    for stanza in range(no_of_stanza):
        stanza = []
        for lines in range(no_of_lines_per_stanza):
            lines = []
            for matra in extracted_pattern:
                vaild_words = find_valid_words(words_list, chhondo, matra)
                lines.append(random.choice(vaild_words)['word'])
            stanza.append(lines)

    # printing output
    # ++++++++++++++++
    for lines in stanza:
        print(" ".join(lines))

    return stanza


if __name__ == "__main__":
    generate_random_poem('database/db/words.json', "4|4|4|2")

# semi-automata: give it a m•n+k sequence, it will recognise all chondo-matra-riti etc
# and then it will construct a new seq with same proerties, and will also match the last syllable of words/lat word to rhyme
