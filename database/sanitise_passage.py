import os
import re

def clean_and_rewrite_file(filename: str):
    with open(filename, "r", encoding="utf-8") as file:
        text = file.read()

    # also remove these: ৷ - = ’ ” ‚
    # Remove English letters, English digits, Bangla digits, and symbols
    cleaned_text = re.sub(r'[a-zA-Z0-9০-৯]', '', text)  # Remove English letters, digits, and Bangla digits
    cleaned_text = re.sub(r'[^\u0980-\u09FF\s]', '', cleaned_text)  # Remove non-Bangla characters except space

    # Split into words and remove duplicates while maintaining order
    words = cleaned_text.split()
    unique_words = list(dict.fromkeys(words))

    # Rewrite the file with cleaned and unique words
    with open(filename, "w", encoding="utf-8") as file:
        file.write(" ".join(unique_words))

file = os.path.join(os.getcwd(), "database", "passage.txt")
clean_and_rewrite_file(file)
