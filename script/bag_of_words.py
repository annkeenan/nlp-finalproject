from script import clean_words
from script.db import Database_Connection

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
                self._word_count[word] = [0] * 5
            self._word_count[word][review['stars']-1] += 1

    # Clean and compile the words in the dict
    def compile_words(self, test=None):
        if test:
            self._word_count = test
        new_word_count = dict()
        for word, rating_count in self._word_count.items():
            new_words = clean_words.clean_word(word)
            for new_word in new_words:
                if new_word not in new_word_count:
                    new_word_count[new_word] = [0] * 5
                for r in range(len(rating_count)):
                    new_word_count[new_word][r] += rating_count[r]
        self._word_count = new_word_count

    # Process reviews into a bag of words
    def count_words(self, range_min=None, range_max=None):
        sql = "SELECT r.text, r.stars FROM review r JOIN business b ON b.id=r.business_id"
        if range_min and range_max:
            sql += " AND b.review_count>=%s AND b.review_count<=%s"
            reviews = self._db_conn.query(sql,[range_min, range_max])
        elif range_min:
            sql += " AND b.review_count>=%s"
            reviews = self._db_conn.query(sql,[range_min])
        elif range_max:
            sql += " AND b.review_count<=%s"
            reviews = self._db_conn.query(sql,[range_max])
        else:
            reviews = self._db_conn.query(sql)
        for review in reviews:
            process_review(self._word_count, review)
        self.compile_words()
