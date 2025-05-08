import os
import re
import json
import random
# from itertools import combinations
from typing import List, Dict, Tuple, Any

class PoemGenerator:
    database_path = 'database/db/words.json'

    def __init__(self, pattern:str = '4|4|2'):
        # pattern stays fixed for an object, cuz high computational load
        self.pattern = pattern

    def determine_chhondo(self, pattern) -> Tuple[str, List[int]]:
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

    def find_valid_words(self, words_list:List[Dict[str, Any]], chhondo:str, matra:int) -> List[Dict[str, Any]]:
        return [w for w in words_list if w['totalMatra'].get(chhondo, 0) == matra]

    def get_allowed_splits(self, m: int) -> List[List[int]]:
        match m:
            case 2 | 3:
                return [[m]]
            case 4:
                return [[4], [2, 2]]
            case 5:
                return [[5], [2, 3]]
            case 6:
                return [[6], [2, 4]]
            case 7:
                return [[7], [2, 5]]
            case 8:
                return [[8], [2, 6], [4, 4]]
            case _:
                return [[m]]   # x > 8

    def find_valid_combinations(self, words_list:List[Dict[str, Any]], chhondo:str, matra:int) -> List[List[List[Dict[str, Any]]]]:
        """
        Returns, for each allowed split of `matra`, the lists of words matching each piece.
        E.g. for matra=6 you get two entries:
          [ [[words of matra=6]] , [[words of matra=2],[words of matra=4]] ]
        """
        # 1) Build matra→words map in one pass
        matra_to_words: Dict[int, List[Dict[str, Any]]] = {}
        for w in words_list:
            m = w['totalMatra'].get(chhondo, 0)
            if m > 0:
                matra_to_words.setdefault(m, []).append(w)

        # 2) Get your splits
        splits = self.get_allowed_splits(matra)

        # 3) For each split, grab the precomputed lists
        results: List[List[List[Dict[str, Any]]]] = []
        for split in splits:
            # for each element in split, pull list of words (may be empty)
            grouped = [ matra_to_words.get(piece, []) for piece in split ]
            results.append(grouped)

        return results

    def generate_random_poem(self, lines_to_generate:int = 2, match_last:bool = False):
        chhondo, extracted_pattern = self.determine_chhondo(self.pattern)

        if not isinstance(lines_to_generate, int):
            print("Invalid input: stanza count and lines per stanza must be integers")
            return
        lines_to_generate = min(8, lines_to_generate) # max 8


        # loading words database
        # +++++++++++++++++++++++++
        words_data = None
        with open(self.database_path, 'r') as f:
            words_data = json.load(f)

        if not words_data or not words_data.get("words"):
            print("Unable to retrive json words data")
            return

        words_list = words_data.get("words")

        # creating poem
        # +++++++++++++++++
        global_words_storage: Dict[str, Any] = {
            # will use self.something in class
        }
        poem = []
        lines = []
        is_odd_line = True # 1st - 3rd -  line
        last_word_of_last_line = ''
        for _ in range(lines_to_generate):
            lines = []
            for matra in extracted_pattern: # [eg 4 4 2]
                '''
                valid_words = find_valid_words(words_list, chhondo, matra)
                random_word = None
                if match_last and not is_odd_line:
                    random_word = random.choice([w for w in valid_words if w['word'][-1] == last_word_of_last_line[-1]])
                        # matching the last letter only, works fine for matra 2, else need to check longer strips
                else:
                    random_word = random.choice(valid_words)

                lines.append(random_word['word'])
                '''

                # store the generated words, cuz matra remains const most of the time,
                global_words_storage['matra'] = matra
                global_words_storage['words'] = self.find_valid_combinations(words_list, chhondo, matra)

                valid_words_list = self.find_valid_combinations(words_list, chhondo, matra)

                word_list = random.choice(valid_words_list)
                lines.extend([w['word'] for w in word_list])

            poem.append(" ".join(lines))
            is_odd_line = not is_odd_line
            last_word_of_last_line = lines[-1]

        return poem


if __name__ == "__main__":
    pattern = "4|4|4|2"
    lines_to_generate=4
    match_last=True

    pg = PoemGenerator(pattern)
    poem = pg.generate_random_poem(lines_to_generate, match_last)

    op_file = os.path.join(os.getcwd(),'generate-poem','poem-op.txt')

    with open(op_file, 'a') as f:
        f.write(f"\n{pattern}\n----------\n")
        for line in poem:
            f.write(f"{line}\n")
        f.write('\n')

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
