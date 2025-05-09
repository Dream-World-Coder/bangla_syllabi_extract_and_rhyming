import os
import re
import json
import random
from typing import List, Dict, Tuple, Any

class PoemGenerator:
    database_path = 'database/db/words.json'
    words_cache: Dict[Tuple[str,int], List[Dict[str, Any]]] = {}

    def __init__(self, pattern: str = '4|4|2'):
        self.pattern = pattern

    def determine_chhondo(self, pattern: str) -> Tuple[str, List[int]]:
        if not pattern or not re.fullmatch(r'(\d+\|)*\d+', pattern):
            raise Exception("Invalid pattern format. Use numbers separated by '|' e.g. 4|4|2")
        extracted = list(map(int, pattern.split('|')))
        max_m = max(extracted)
        if max_m <= 4:
            ch = 'স্বরবৃত্ত'
        elif max_m <= 7:
            ch = 'মাত্রাবৃত্ত'
        else:
            ch = 'অক্ষরবৃত্ত'
        return ch, extracted

    def find_valid(self, words: List[Dict[str, Any]], ch: str, m: int, pos: str = None) -> List[Dict[str, Any]]:
        key = (ch, m)
        if key not in self.words_cache:
            self.words_cache[key] = [w for w in words if w['totalMatra'].get(ch,0)==m]
        cand = self.words_cache[key]
        if pos:
            pos_cand = [w for w in cand if w.get('pos')==pos]
            return pos_cand or cand
        return cand

    def load_words(self) -> List[Dict[str,Any]]:
        with open(self.database_path) as f:
            data = json.load(f)
        return data.get('words', [])


pg = PoemGenerator(pattern='4|4|2')
for line in pg.generate_poem_with_grammar():
    print(line)
