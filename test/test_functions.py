# test_functions.py
import unittest
from context import script
from script import functions
from script.db import Database_Connection

class TestFunctions(unittest.TestCase):

    def test_clean_word(self):
        words = ['test?','test":;','test\'s','\'test','test-test','test\n','TEST']
        exp_words = [['test','?'],['test'],['test\'s'],['test'],['test','test'],['test'],['test']]
        for w in range(len(words)):
            new_word = functions.clean_word(words[w])
            self.assertEqual(new_word, exp_words[w])

    def test_correctness(self):
        ratings = [
            {'pred':5, 'obsv':4},
            {'pred':5, 'obsv':5}
        ]
        exp_correctness = 0.5
        correctness = functions.correctness(ratings)
        self.assertEqual(correctness, exp_correctness)

    def test_baseline_correctness(self):
        db_conn = Database_Connection()
        correctness = functions.baseline_correctness(db_conn=db_conn, test=True)
        self.assertIsInstance(correctness, float)

    def test_calculate_stddev(self):
        ratings = [
            {'pred':5, 'obsv':4},
            {'pred':5, 'obsv': 3}
        ]
        exp_stddev = 2.2360679775
        stddev = functions.calculate_stddev(ratings)
        self.assertAlmostEqual(stddev, exp_stddev)

    def test_baseline_stddev(self):
        db_conn = Database_Connection()
        stddev = functions.baseline_stddev(db_conn=db_conn, test=True)
        self.assertIsInstance(stddev, float)

    def test_get_reviews(self):
        db_conn = Database_Connection()
        reviews = functions.get_reviews(db_conn=db_conn, test=True)
        self.assertIsInstance(reviews, list)

if __name__ == '__main__':
    unittest.main()
