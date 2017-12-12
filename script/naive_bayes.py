# naive_bayes.py
import math
from script import functions
from collections import defaultdict

SCALE = 5  # rating scale 1-5


class BagOfPhrases(object):

    def __init__(self, n=1):
        self._phrase_count = defaultdict(dict)
        self._obs_phrases = set()
        self._n = n  # default unigram

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
                self._phrase_count[phrase][r] = rating_count[r] / sum_count

    # Process reviews into a bag of words
    def count_phrases(self, load_file):
        with open(load_file) as lf:
            for line in lf:
                l = line.rstrip().split(' ')
                # error checking
                if len(l) < 2:
                    break
                # initial start word
                phrase_list = [functions.START] * (self._n-1)
                # iterate through the review
                for word in l[1:]:
                    # construct the new phrase
                    phrase_list.append(word)
                    phrase = tuple(phrase_list)
                    # handle new word
                    if phrase not in self._obs_phrases:
                        self._obs_phrases.add(phrase)
                        self._phrase_count[phrase] = [0] * SCALE
                    self._phrase_count[phrase][int(l[0])-1] += 1
                    phrase_list.pop(0)  # prepare for the next word

    # Predict the rating of a review
    def predict(self, review):
        counts = [0] * SCALE  # stores the log probabilities for each rating
        phrase_list = [functions.START] * (self._n-1)
        for word in review:
            phrase_list.append(word)
            phrase = tuple(phrase_list)
            # if word in training data
            if phrase in self._phrase_count:
                for c in range(SCALE):
                    counts[c] += self._phrase_count[phrase][c]
            phrase_list.pop(0)
        # choose the first of the list if there is a tie
        max_indices = [i for i, j in enumerate(counts) if j == max(counts)]
        return max_indices[0] + 1
