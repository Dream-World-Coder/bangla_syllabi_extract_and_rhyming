import os
import re

def clean_and_rewrite_file(filename: str):
    with open(filename, "r", encoding="utf-8") as file:
        text = file.read()

    # Remove English letters, English digits, Bangla digits,
    # plus the Bengali danda (৷), hyphen (-), equals (=), ’, ”, ‚
    cleaned_text = re.sub(
        r"[a-zA-Z0-9০-৯\u09F7\-=’”‚]",
        "",
        text
    )
    # Now remove any remaining non‑Bangla (U+0980–U+09FF) characters except whitespace
    cleaned_text = re.sub(r"[^\u0980-\u09FF\s]", "", cleaned_text)

    # Split into words and remove duplicates while maintaining order
    words = cleaned_text.split()
    unique_words = list(dict.fromkeys(words))

    # Rewrite the file with cleaned and unique words
    with open(filename, "w", encoding="utf-8") as file:
        file.write(" ".join(unique_words))

if __name__ == "__main__":
    file = os.path.join(os.getcwd(), "database", "passage.txt")
    clean_and_rewrite_file(file)
