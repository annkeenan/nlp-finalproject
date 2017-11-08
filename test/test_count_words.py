# test_word_count.py
import unittest
from context import script
from script import count_words, db

class TestCountWords(unittest.TestCase):

    def test_process_review(self):
        word_count = dict()
        reviews = [
            {'stars': 5,'text':'test1 test'},
            {'stars': 4,'text':'test test2'},
            {'stars': 2,'text':'test2 test1'},
            {'stars': 4,'text':'test test1'}
        ]
        exp_word_count = {
            'test':[0,0,0,2,1],
            'test1':[0,1,0,1,1],
            'test2':[0,1,0,1,0],
        }
        for review in reviews:
            count_words.process_review(word_count, review)
        self.assertEqual(word_count, exp_word_count)

    def test_count_words(self):
        db_conn = db.Database_Connection()
        word_count = count_words.count_words(db_conn=db_conn,range_max=1)
        word_count_both = count_words.count_words(db_conn,1,1)
        self.assertIsInstance(word_count, dict)
        self.assertIsInstance(word_count_both, dict)

if __name__ == '__main__':
    unittest.main()
