# naive_bayes.py
import math
from script import functions
from collections import defaultdict

SCALE = 5  # rating scale 1-5


class BagOfPhrases(object):

    def __init__(self, n=1):
        self._obs_phrases = set()
        self._n = n  # default unigram
        self._phrase_count = defaultdict(list)
        self.multiplier = []
        m = 2
        for i in range(n):
            m = math.pow(m, 2)
            self.multiplier.append(m)

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
                # skip incorrectly formatted lines
                if len(l) < 2:
                    continue

                # initial start words
                phrase_list = []
                for i in range(self._n):  # index as the number of previous words tracked
                    phrase_list.append([functions.START] * i)

                # iterate through the review
                for word in l[1:]:
                    # construct the new phrase
                    phrases = []
                    for i in range(self._n):
                        phrase_list[i].append(word)
                        phrases.append(tuple(phrase_list[i]))

                    for phrase in phrases:
                        # handle new word
                        if phrase not in self._obs_phrases:
                            self._obs_phrases.add(phrase)
                            self._phrase_count[phrase] = [0] * SCALE
                        self._phrase_count[phrase][int(l[0])-1] += 1

                    # prepare for the next word
                    for i in range(self._n):
                        phrase_list[i].pop(0)

    # Predict the rating of a review
    def predict(self, review):
        counts = [0] * SCALE  # stores the probabilities for each rating

        # initial start words
        phrase_list = []
        for i in range(self._n):  # index as the number of previous words tracked
            phrase_list.append([functions.START] * i)

        for word in review:
            # construct the new phrase
            phrases = []
            for i in range(self._n):
                phrase_list[i].append(word)
                phrases.append(tuple(phrase_list[i]))

            # stores the probabilities for each rating at each gram level
            smoothed_counts = []
            for i in range(self._n):
                smoothed_counts.append([0] * SCALE)

            for i, phrase in enumerate(phrases):
                # if phrase in training data
                if phrase in self._phrase_count:
                    for c in range(SCALE):
                        smoothed_counts[i][c] += self._phrase_count[phrase][c]

            # smooth and add to counts
            for m, smcounts in enumerate(smoothed_counts):
                for i, count in enumerate(smcounts):
                    counts[i] += count*self.multiplier[m]

            # prepare for the next word
            for i in range(self._n):
                phrase_list[i].pop(0)

        # choose the first of the list if there is a tie
        max_indices = [i for i, j in enumerate(counts) if j == max(counts)]
        return max_indices[0] + 1
