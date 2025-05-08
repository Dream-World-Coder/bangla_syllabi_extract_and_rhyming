import re

def clean_and_rewrite_file(filename: str):
    with open(filename, "r", encoding="utf-8") as file:
        text = file.read()

    # Remove specified punctuation
    cleaned_text = re.sub(r'[,\.\|;।_•৽。\u200C]', '', text)

    # Split into words and remove duplicates while maintaining order
    words = cleaned_text.split()
    unique_words = list(dict.fromkeys(words))  # Preserves order while removing duplicates

    # Rewrite the file with cleaned and unique words
    with open(filename, "w", encoding="utf-8") as file:
        file.write(" ".join(unique_words))

# Run the function on "dataset.txt"
clean_and_rewrite_file("dataset.txt")
