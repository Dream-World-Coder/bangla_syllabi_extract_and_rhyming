class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end = False
        # you can store additional info (like frequency or complete words) if needed

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word):
        """Inserts a word into the trie."""
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end = True

    def search(self, word):
        """Returns True if the word is in the trie."""
        node = self.root
        for char in word:
            if char not in node.children:
                return False
            node = node.children[char]
        return node.is_end

    def starts_with(self, prefix):
        """Returns all words in the trie that start with the given prefix."""
        node = self.root
        for char in prefix:
            if char not in node.children:
                return []
            node = node.children[char]
        results = []
        self._dfs(node, prefix, results)
        return results

    def _dfs(self, node, path, results):
        if node.is_end:
            results.append(path)
        for char, child in node.children.items():
            self._dfs(child, path + char, results)

class TrieDictionary:
    def __init__(self):
        # One trie for normal prefix search.
        self.prefix_trie = Trie()
        # Another trie for suffix search, storing reversed words.
        self.suffix_trie = Trie()

    def add_word(self, word):
        """Adds a word/syllable to both tries."""
        self.prefix_trie.insert(word)
        reversed_word = word[::-1]
        self.suffix_trie.insert(reversed_word)

    def load_from_file(self, file_path):
        """Loads words from a file (one word per line) and inserts into the dictionary."""
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                word = line.strip()
                if word:  # skip empty lines
                    self.add_word(word)

    def search(self, word):
        """Exact word search."""
        return self.prefix_trie.search(word)

    def prefix_search(self, prefix):
        """Search words with the given prefix."""
        return self.prefix_trie.starts_with(prefix)

    def suffix_search(self, suffix):
        """Search words ending with the given suffix.
           This is done by reversing the suffix and using prefix search on the reversed trie.
        """
        reversed_suffix = suffix[::-1]
        reversed_matches = self.suffix_trie.starts_with(reversed_suffix)
        # reverse back the found words
        return [word[::-1] for word in reversed_matches]

# Example usage:
if __name__ == "__main__":
    trie_dict = TrieDictionary()

    # Example words/syllables (Bengali words/syllables; you can replace these with actual Bengali content)
    words = ["বাংলা", "ভাষা", "শব্দ", "স্বর", "সঙ্গীত", "পাঠ", "পাঠ্য"]
    for w in words:
        trie_dict.add_word(w)

    print("Search for exact word 'বাংলা':", trie_dict.search("বাংলা"))
    print("Prefix search for 'পা':", trie_dict.prefix_search("পা"))
    print("Suffix search for 'ষা':", trie_dict.suffix_search("ষা"))

    # To load from a file, create a text file (e.g., 'bengali_words.txt') with one word per line:
    # trie_dict.load_from_file('bengali_words.txt')
