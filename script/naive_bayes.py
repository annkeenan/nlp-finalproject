# naive_bayes.py
import math
from script import functions
from collections import defaultdict

SCALE = 5  # rating scale 1-5


# Classic Naive Bayes
class BagOfWords(object):

    def __init__(self):
        self._word_count = dict()
        self._obs_words = set()

    # Return the private variable
    def get_word_count(self):
        return self._word_count

    # Call relevant functions to create a bag of words
    def construct(self, load_file):
        self.count_words(load_file)
        self.convert_counts()

    # Convert counts to log probabilities
    def convert_counts(self):
        for word, rating_count in self._word_count.items():
            rating_count = [r + .1 for r in rating_count]
            sum_count = sum(rating_count)
            for r in range(SCALE):
                self._word_count[word][r] = math.log(
                    rating_count[r] / sum_count, 2)

    # Process reviews into a bag of words
    def count_words(self, load_file):
        with open(load_file) as lf:
            for line in lf:
                l = line.rstrip().split(' ')
                for word in l[1:]:
                    if word not in self._obs_words:
                        self._obs_words.add(word)
                        self._word_count[word] = [0] * SCALE
                    self._word_count[word][int(l[0])-1] += 1

    # Predict the rating of a review
    def predict(self, review):
        counts = [0] * SCALE  # stores the log probabilities for each rating
        for word in review:
            # if word is in the training data
            if word in self._word_count.keys():
                for c in range(SCALE):
                    counts[c] += self._word_count[word][c]
        max_indices = [i for i, j in enumerate(counts) if j == max(counts)]
        return max_indices[0] + 1


# Naive Bayes with a bigram approach
class BagOfPhrases(object):

    def __init__(self, n):
        self._phrase_count = defaultdict(dict)
        self._obs_phrases = set()

    # Return the private variable
    def get_phrase_count(self):
        return self._phrase_count

    # Call relevant functions to create a bag of words
    def construct(self, load_file):
        self.count_phrases(load_file)
        self.convert_counts()

    # Convert counts to log probabilities
    def convert_counts(self):
        for phrase, rating_count in self._phrase_count.items():
            rating_count = [r + .1 for r in rating_count]
            sum_count = sum(rating_count)
            for r in range(SCALE):
                self._phrase_count[phrase][r] = math.log(
                    rating_count[r] / sum_count, 2)

    # Process reviews into a bag of words
    def count_phrases(self, load_file):
        with open(load_file) as lf:
            for line in lf:
                l = line.rstrip().split(' ')
                if len(l) < 2:
                    break
                prev_word = functions.START
                for word in l[1:]:
                    phrase = (prev_word, word)
                    if phrase not in self._obs_phrases:
                        self._obs_phrases.add(phrase)
                        self._phrase_count[phrase] = [0] * SCALE
                    self._phrase_count[phrase][int(l[0])-1] += 1

    # Predict the rating of a review
    def predict(self, review):
        counts = [0] * SCALE  # stores the log probabilities for each rating
        prev_word = functions.START
        for word in review:
            phrase = (prev_word, word)
            # if word is in the training data
            if phrase in self._phrase_count.keys():
                for c in range(SCALE):
                    counts[c] += self._phrase_count[phrase][c]
        # choose the first of the list if there is a tie
        max_indices = [i for i, j in enumerate(counts) if j == max(counts)]
        return max_indices[0] + 1
