from itertools import combinations
from typing import List, Dict,Tuple, Any

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


def _find_valid_combinations(words_list, chhondo, matra, max_words=1)->list[list[dict[str, Any]]]:
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


def get_allowed_splits(m: int) -> List[List[int]]:
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

def __find_valid_combinations(words_list: List[Dict[str, Any]], chhondo: str, matra: int, max_words=1) -> List[List[Dict[str, Any]]]:
    results = []

    # Filter and group words by their matra value
    filtered_words = [w for w in words_list if w['totalMatra'].get(chhondo, 0) > 0]
    matra_to_words = {}
    for word in filtered_words:
        m = word['totalMatra'][chhondo]
        if m not in matra_to_words:
            matra_to_words[m] = []
        matra_to_words[m].append(word)

    allowed_splits = get_allowed_splits(matra)

    for split in allowed_splits:
        if len(split) > max_words:
            continue

        def backtrack(index, path, used_ids):
            if index == len(split):
                results.append(path[:])
                return
            m = split[index]
            for word in matra_to_words.get(m, []):
                if id(word) in used_ids:
                    continue  # prevent reusing the same word object
                path.append(word)
                used_ids.add(id(word))
                backtrack(index + 1, path, used_ids)
                path.pop()
                used_ids.remove(id(word))

        backtrack(0, [], set())

    return results
