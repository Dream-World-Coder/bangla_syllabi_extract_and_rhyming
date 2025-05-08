import os
import re
import json
import random
from typing import List, Dict, Tuple, Any

class PoemGenerator:
    database_path = 'database/db/words.json'
    words_cache: Dict[int, List[Dict[str, Any]]] = {}  # cache valid words by matra

    def __init__(self, pattern: str = '4|4|2'):
        self.pattern = pattern

    def determine_chhondo(self, pattern) -> Tuple[str, List[int]]:
        if not pattern:
            raise Exception("pattern not found")
        if not re.fullmatch(r'(\d+\|)*\d+', pattern):
            raise Exception("Invalid pattern format. Use <num>|<num>|...|<num> (e.g., 4|4|4|2)")
        extracted_pattern = list(map(int, pattern.split('|')))
        highest_matra = max(extracted_pattern)
        if highest_matra < 2:
            raise Exception("matra should at least be 2")
        if 2 <= highest_matra <= 4:
            chhondo = "স্বরবৃত্ত"
        elif 5 <= highest_matra <= 7:
            chhondo = "মাত্রাবৃত্ত"
        elif 8 <= highest_matra <= 12:
            chhondo = "অক্ষরবৃত্ত"
        else:
            raise Exception("matra at max can be 10")
        return chhondo, extracted_pattern

    def find_valid_words(self, words_list: List[Dict[str, Any]], chhondo: str, matra: int) -> List[Dict[str, Any]]:
        # fetch from cache if available
        if matra in self.words_cache:
            return self.words_cache[matra]
        valid = [w for w in words_list if w['totalMatra'].get(chhondo, 0) == matra]
        self.words_cache[matra] = valid
        return valid

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
                return [[m]]

    def generate_random_poem(self, lines_to_generate: int = 2, match_last: bool = False) -> List[str]:
        chhondo, extracted_pattern = self.determine_chhondo(self.pattern)
        if not isinstance(lines_to_generate, int):
            raise Exception("Invalid input: stanza count and lines per stanza must be integers")

        # load words once
        with open(self.database_path, 'r') as f:
            data = json.load(f)
        words_list = data.get("words") or []
        if not words_list:
            raise Exception("Unable to retrieve json words data")

        poem = []
        is_odd_line = True
        last_word_of_prev_line = ''

        for _ in range(lines_to_generate):
            used_in_line = set()
            line_words: List[str] = []
            for matra in extracted_pattern:
                # get possible splits
                splits = self.get_allowed_splits(matra)
                # choose a split randomly
                split = random.choice(splits)
                # for each piece in split, pick a word
                for idx, piece in enumerate(split):
                    candidates = self.find_valid_words(words_list, chhondo, piece)
                    # avoid duplicates in same line
                    fresh = [w for w in candidates if w['word'] not in used_in_line]
                    if not fresh:
                        fresh = candidates
                    # if match_last for last piece in even line
                    if match_last and not is_odd_line and idx == len(split) - 1 and last_word_of_prev_line:
                        last_char = last_word_of_prev_line[-1]
                        matched = [w for w in fresh if w['word'].endswith(last_char)]
                        if matched:
                            fresh = matched
                    if not fresh:
                        raise Exception(f"No words available for matra {piece}")
                    choice = random.choice(fresh)
                    used_in_line.add(choice['word'])
                    line_words.append(choice['word'])
            poem.append(" ".join(line_words))
            is_odd_line = not is_odd_line
            last_word_of_prev_line = line_words[-1]
        return poem


if __name__ == "__main__":
    pattern = "4|4|4|2"
    lines_to_generate = 4
    match_last = True
    pg = PoemGenerator(pattern)
    poem = pg.generate_random_poem(lines_to_generate, match_last)
    out_dir = os.path.join(os.getcwd(), 'generate-poem')
    os.makedirs(out_dir, exist_ok=True)
    op_file = os.path.join(out_dir, 'poem-op.txt')
    with open(op_file, 'a', encoding='utf-8') as f:
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
