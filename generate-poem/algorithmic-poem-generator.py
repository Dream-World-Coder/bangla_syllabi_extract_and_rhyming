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
                # ---
            case 5:
                return [[5], [2, 3], [1, 4]]
            case 6:
                return [[2, 4], [3, 3]]
            case 7:
                return [[2, 5], [3, 4]]
                # ---
            case 8:
                return [[5, 3], [2, 6], [4, 4]]
            case 9:
                return [[3, 6], [4, 5]]
            case 10:
                return [[3,4,3], [4, 6], [5, 5]]
            case _:
                return [[m]]

    def generate_random_poem(self, lines_to_generate: int = 2, match_last: bool = True) -> List[str]:
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

    def generate_poem_with_grammar(self):
        # lines_to_generate: int = 2, not to be as param
        # first check the self.pattern,
        # chhondo, extracted_pattern = self.determine_chhondo(self.pattern)
        # the sentence will have len(extracted_pattern) words [for now, later i will wrap a sentence in 2-4 lines, for more poetic feel]
        # so make the sentence with the grammar,
        # eg final sentence = <NOUN> <NOUN> <VERB> <ADJ> <NOUN>
        # now we know the matra and chhondo, but as we also have access to POS now, we will look por word.POS and match the resultant sentence
        # this is the only difference from generate_random_poem, that is consideration of the word.POS alongside word.totalMatra.chhondo
        # NOW MAKE IT, CAREFULLY OBSERVE THE generate_random_poem

        # ——————————————————————
        # 1) determine chhondo & pattern
        chhondo, extracted_pattern = self.determine_chhondo(self.pattern)
        L = len(extracted_pattern)

        # 2) define a tiny POS-sequence grammar for child-poem feel
        grammar_rules: Dict[int, List[str]] = {
            2: ["NOUN", "VERB"],
            3: ["NOUN", "ADJ", "NOUN"],
            4: ["ADJ", "NOUN", "VERB", "ADJ"],
            5: ["NOUN", "NOUN", "VERB", "ADJ", "NOUN"],
            # extend as needed...
        }
        if L not in grammar_rules:
            raise Exception(f"No grammar rule for sentence length {L}")

        pos_sequence = grammar_rules[L]

        # 3) load word database
        with open(self.database_path, 'r') as f:
            data = json.load(f)
        words_list = data.get("words") or []
        if not words_list:
            raise Exception("Unable to retrieve json words data")

        # 4) pick one word per slot
        used = set()
        sentence_tokens: List[str] = []

        for idx, matra in enumerate(extracted_pattern):
            desired_pos = pos_sequence[idx]
            # matra-filtered
            candidates = self.find_valid_words(words_list, chhondo, matra)
            # POS-filtered
            pos_candidates = [w for w in candidates if w.get("pos") == desired_pos]
            pool = pos_candidates or candidates  # fallback if no POS match
            # avoid repetition
            fresh = [w for w in pool if w["word"] not in used] or pool
            if not fresh:
                raise Exception(f"No words for matra={matra}, POS={desired_pos}")
            choice = random.choice(fresh)
            used.add(choice["word"])
            sentence_tokens.append(choice["word"])

        # 5) return the joined sentence
        return " ".join(sentence_tokens)

if __name__ == "__main__":
    pattern = "7|7|7|2"
    lines_to_generate = 4
    match_last = True
    pg = PoemGenerator(pattern)
    poem = pg.generate_poem_with_grammar()
    out_dir = os.path.join(os.getcwd(), 'generate-poem')
    os.makedirs(out_dir, exist_ok=True)
    op_file = os.path.join(out_dir, 'output.txt')
    with open(op_file, 'a', encoding='utf-8') as f:
        f.write(f"\n{pattern} WITH GRAMMAR\n----------\n")
        f.write(f"{"".join(poem)}\n")
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
