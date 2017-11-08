# bag_of_words.py
from script import functions
from script.db import Database_Connection

SCALE = 5 # rating scale 1-5

class BagOfWords(object):
    def __init__(self):
        self._db_conn = Database_Connection()
        self._word_count = dict()

    def get_word_count(self):
        return self._word_count

    # Process the review into words
    def process_review(self, review):
        for word in review['text'].split(' '):
            if word not in self._word_count:
                self._word_count[word] = [0] * SCALE
            self._word_count[word][review['stars']-1] += 1

    # Clean and compile the words in the dict
    def compile_words(self, test=None):
        if test:
            self._word_count = test
        new_word_count = dict()
        for word, rating_count in self._word_count.items():
            new_words = functions.clean_word(word)
            for new_word in new_words:
                if new_word not in new_word_count:
                    new_word_count[new_word] = [0] * SCALE
                for r in range(SCALE):
                    new_word_count[new_word][r] += rating_count[r]
        self._word_count = new_word_count

    # Process reviews into a bag of words
    def count_words(self, range_max=None, test=None):
        reviews = functions.get_reviews(db_conn=self._db_conn, range_max=range_max, test=test)
        for review in reviews:
            self.process_review(review)
        self.compile_words() # automatically compile the counts

    # Predict the rating of a sentence
    def predict(self, sentence, test=None):
        if test:
            self._word_count = test
        counts = [0] * SCALE
        cleaned_sentence = []
        for word in sentence.split(' '):
            cleaned_sentence.extend(functions.clean_word(word))
        for word in cleaned_sentence:
            if word in self._word_count.keys():
                for c in range(SCALE):
                    counts[c] += self._word_count[word][c]
        prediction = 0
        num_counts = 0
        for c in range(len(counts)):
            prediction += counts[c] * (c+1)
            num_counts += counts[c]
        return prediction/num_counts
