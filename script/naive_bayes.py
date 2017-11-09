# naive_bayes.py
import enchant
import math
from script import functions
from script.db import Database_Connection

SCALE = 5 # rating scale 1-5

class BagOfWords(object):

    def __init__(self):
        self._db_conn = Database_Connection()
        self._word_count = dict()
        self._Dict = Dict = enchant.Dict("en_US")
        self._convert = False

    def save(self, filename):
        with open(filename, 'w') as f:
            for word, ratings in self._word_count.items():
                f.write('%s ' % word)
                for r in ratings:
                    f.write('%f,' % r)
                f.write('\n')

    def load(self, filename):
        self._convert = True
        with open(filename, 'r') as f:
            for line in f:
                l = line.rstrip().split(' ')
                self._word_count[l[0]] = l[1].split(',')[:5]#[float(r) for r in l[1].split(',')[:5]]

    def get_word_count(self):
        return self._word_count

    def construct(self, range_max=None, test=None):
        self.count_words(range_max, test)
        self.convert_counts()

    # Process the review into words
    def process_review(self, review):
        for word in functions.clean_review(review['text'], self._Dict):
            if word not in self._word_count:
                self._word_count[word] = [0] * SCALE
            self._word_count[word][review['stars']-1] += 1

    # Convert counts to log probabilities
    def convert_counts(self, test=None):
        if test:
            self._word_count = test
        for word, rating_count in self._word_count.items():
            rating_count = [r + .1 for r in rating_count]
            sum_count = sum(rating_count)
            for r in range(SCALE):
                self._word_count[word][r] = math.log(rating_count[r]/sum_count, 2)

    # Process reviews into a bag of words
    def count_words(self, range_max=None, test=None):
        reviews = functions.get_reviews(db_conn=self._db_conn, range_max=range_max, test=test)
        for review in reviews:
            self.process_review(review)

    # Predict the rating of a review
    def predict(self, review, test=None):
        if test:
            self._word_count = test
        counts = [0] * SCALE # stores the log probabilities for each rating
        for word in functions.clean_review(review, self._Dict):
            if word in self._word_count.keys():
                for c in range(SCALE):
                    if self._convert:
                        counts[c] += float(self._word_count[word][c])
                    else:
                        counts[c] += self._word_count[word][c]
        max_indices = [i for i, j in enumerate(counts) if j == max(counts)]
        return max_indices[0] + 1
