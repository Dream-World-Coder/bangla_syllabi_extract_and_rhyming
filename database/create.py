from splitting import SplitBanglaSyllabi

splitter = SplitBanglaSyllabi()

read_file = "dataset.txt"
write_file = "db/words.txt"
# write_file = "db/words.json"

'''
// SCHEMA
table/document: 'words'

    word{
        exact_word_with_suffix_search
        length
        syllabi:[
            syllable:'name'
        ]
    }

'''

content = ""

with open(read_file, "r") as f:
    content = f.read()

with open(write_file, "w") as f:
    syllabi = splitter.split_sentence_into_syllabi(content)
    f.write("{")
    f.write('\n\t"words" : [')
    for item in syllabi:
        f.write(f"""
        {{
            "word": "{item[0]}",
            "syllabi": [{', '.join(f'"{i}"' for i in item[1])}]
        }},
        """)
    f.write("\t]\n")
    f.write("}")



# i have to put 4n+2 means 4 syllabli * n + 2 syllabi
# or n words with 4 syllabi + one word with 2 syllabi
