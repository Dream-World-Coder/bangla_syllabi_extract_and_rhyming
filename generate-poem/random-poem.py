import os
import re
import json
import random
from itertools import combinations
from typing import Any

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


def __find_valid_words(words_list, chhondo, matra): # not feasible
    # filter words with matra>0
    filtered_words_list = [word for word in words_list if word['totalMatra'].get(chhondo, 0) > 0]

    valid_combinations = []

    # try all possible non-empty combinations
    for r in range(1, len(filtered_words_list) + 1):
        for combo in combinations(filtered_words_list, r):
            total = sum(word['totalMatra'][chhondo] for word in combo)
            if total == matra:
                valid_combinations.append(combo)

    return valid_combinations


def find_valid_combinations(words_list, chhondo, matra, max_words=1)->list[list[dict[str, Any]]]:
    results = []

    # Preprocess: keep only words with positive matra for given chhondo
    valid_words = [w for w in words_list if w['totalMatra'].get(chhondo, 0) > 0]
    valid_words.sort(key=lambda w: w['totalMatra'][chhondo])  # optional but helps with pruning

    def backtrack(start, path, current_sum):
        if current_sum == matra:
            results.append(path[:])
            return
        if current_sum > matra or len(path) >= max_words:
            return

        for i in range(start, len(valid_words)):
            word = valid_words[i]
            mat = word['totalMatra'][chhondo]
            if current_sum + mat > matra:
                break  # pruning
            path.append(word)
            backtrack(i + 1, path, current_sum + mat)
            path.pop()

    backtrack(0, [], 0)
    return results


def generate_random_poem(db_path:str, pattern:str, no_of_lines_per_stanza:int=2, no_of_stanza:int=1, match_last=False):
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
    lines = []
    is_odd_line = True # 1st - 3rd -  line
    last_word_of_last_line = ''
    for _ in range(no_of_stanza):
        stanza = []
        for _ in range(no_of_lines_per_stanza):
            lines = []
            for matra in extracted_pattern:
                valid_words = find_valid_words(words_list, chhondo, matra)

                random_word = None
                if match_last and not is_odd_line:
                    random_word = random.choice([w for w in valid_words if w['word'][-1] == last_word_of_last_line[-1]])
                        # matching the last letter only, works fine for matra 2, else need to check longer strips
                else:
                    random_word = random.choice(valid_words)

                lines.append(random_word['word'])

                # valid_words_list = find_valid_combinations(words_list, chhondo, matra, 8)
                # word_list = random.choice(valid_words_list)
                # lines.extend([w['word'] for w in word_list])
            stanza.append(lines)
            is_odd_line = not is_odd_line
            last_word_of_last_line = lines[-1]

    # printing output
    # ++++++++++++++++
    for lines in stanza:
        print(" ".join(lines))

    return stanza



if __name__ == "__main__":
    pattern = "5|5|5|2"
    stanza = generate_random_poem('database/db/words.json', pattern, match_last=True) or []

    op_file = os.path.join(os.getcwd(),'generate-poem','poem-op.txt')

    with open(op_file, 'a') as f:
        f.write(f"\n{pattern}\n----------\n")
        for lines in stanza:
            f.write(f"{" ".join(lines)}\n")
        f.write('\n')

# semi-automata: give it a m•n+k sequence, it will recognise all chondo-matra-riti etc || give it svo str & it will constract a new
# and then it will construct a new seq with same proerties, and will also match the last syllable of words/lat word to rhyme

# matra     s-b     m-b     a-b
# 1     :   1380    920     668
# 2     :   9231    1943    5235
# 3     :   7267    4690    8822
# 4     :   3170    5237    5095
# 5     :   817     4145    1712
# 6     :   189     2359    470
# 7     :   59      1644    94
# 8     :   14      806     32
# 9     :   10      394     10
# 10    :   2       222     6
# 11    :   1       88      1
# 12    :   2       40      2
# 13    :   0       33      1
# 14    :   0       10      0
# 15    :   0       7       0
# 16    :   0       6       1
# 17    :   0       5       0
