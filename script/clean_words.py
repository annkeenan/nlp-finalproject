# clean_words.py
import re

# Returns a list of the cleaned word(s)
def clean_word(word):
    new_words = []
    words = re.findall(r"[\w'?!\\]+", word)
    for word in words:
        new_word = ''
        for w in range(len(word)):
            # skip escaped words
            if word[w] == '\\':
                w += 1
            # character expressions to keep
            elif word[w] in '?!':
                if new_word:
                    new_words.append(new_word)
                new_words.append(word[w])
                new_word = ''
            # construct the new word
            else:
                new_word += word[w]
        if new_word:
            new_words.append(new_word)
    return new_words


# Clean an compile the words in the dict
def compile_words(words_count):
    new_words_count = dict()
    for word, rating_count in words_count.items():
        new_words = clean_word(word)
        for new_word in new_words:
            if new_word not in new_words_count:
                new_words_count[new_word] = [0] * 5
            for r in range(len(rating_count)):
                new_words_count[new_word][r] += rating_count[r]
    return new_words_count
