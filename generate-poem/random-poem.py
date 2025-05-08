import re
import json
import random

def generate_random_poem(db_path:str, pattern:str, no_of_lines_per_stanza:int=2, no_of_stanza:int=1):
    # validate db_path
    if not db_path:
        print("database path not found")
        return

    # no_of_lines_per_stanza = 2 (fixed now) # later will expand to 2-8
    # no_of_stanza = any int
    if not isinstance(no_of_stanza, int) or not isinstance(no_of_lines_per_stanza, int):
        print("Invalid input: stanza count and lines per stanza must be integers")
        return

    no_of_lines_per_stanza = 2 # fixing to 2 for now
    no_of_stanza = min(no_of_stanza, 8) # max 8

    # validate pattern & determine ছন্দ from that
    if not pattern:
        print("pattern not found")
        return
    # check pattern structure <num>|<num>|...|<num>
    if not re.fullmatch(r'^(\d+\|)*\d+$', pattern): # ^ ... $ are not needed, for fullMatch
        print("Invalid pattern format. Use <num>|<num>|...|<num> (e.g., 4|4|4|2)")
        return

    extracted_pattern = list(map(int, pattern.split('|')))
    highest_matra = max(extracted_pattern)
    chhondo = ''

    if highest_matra<2:
        print("matra should at least be 2")
        return

    if 2 <= highest_matra <= 4:
        chhondo = "স্বরবৃত্ত"
    elif 5 <= highest_matra <= 7:
        chhondo = "মাত্রাবৃত্ত"
    elif 8 <= highest_matra <= 10+2: # acctually 10 but giving 2 extra for testing results
        chhondo = "অক্ষরবৃত্ত"
    else:
        # chhondo = "undefined"
        print("matra at max can be 10")
        return


    words_data = None
    with open(db_path, 'r') as f:
        words_data = json.load(f)

    if not words_data:
        print("Unable to retrive json words data")
        return

    words_list = words_data.get("words", [])
    if not words_list:
        print("Unable to retrive words list")
        return

    for stanza in range(no_of_stanza):
        for lines in range(no_of_lines_per_stanza):
            for matra in extracted_pattern:
                ...
                # words_list.find =>
                # word or words for which
                # word.totalMatra.[chhondo] = matra
                # or, SumESum(word.totalMatra.[chhondo]) = matra // in sumesum check: matra > 0 must
                # now after you find them, store them temporarily because in most of the cases matra will be repeatitive (eg 7n+2, m*n+k)
                # now:
                    # randomly pic any one [easiest]
                    # check parts of speech (word.partsOfSpeech) & pick any random based on a grammar
                    # check মিল of last word, eg: বনে - মনে
                    # alongside grammar check meaning & correspondance with previous words{something like correlation available here?} also and then pick one [hardest]


if __name__ == "__main__":
    generate_random_poem('database/db/words.json', "4|4|2")
    # similarly make a poem generator which follows grammar
