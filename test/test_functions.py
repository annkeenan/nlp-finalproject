# test_functions.py
# Test the helper functions
import enchant
import unittest
from context import script
from script import functions
from script.db import Database_Connection


class TestFunctions(unittest.TestCase):
    testfile = 'data/data.sample'
    _Dict = enchant.Dict("en_US")

    def test_clean_review(self):
        review = 'test? test":; test\'s \'test test-test test\n TEST prueba'
        exp_words = ['test', 'test', 'test\'s',
                     'test', 'test', 'test', 'test', 'test']
        words = functions.clean_review(review, self._Dict)
        self.assertEqual(words, exp_words)

    def test_accuracy(self):
        ratings = [(5, 4), (5, 5)]
        exp_accuracy = 0.5
        accuracy = functions.accuracy(ratings)
        self.assertEqual(accuracy, exp_accuracy)

    def test_baseline_accuracy(self):
        accuracy = functions.baseline_accuracy(self.testfile)
        self.assertIsInstance(accuracy, float)

    def test_calculate_stddev(self):
        ratings = [(5, 4), (5, 3)]
        exp_stddev = 2.2360679775
        stddev = functions.calculate_stddev(ratings)
        self.assertAlmostEqual(stddev, exp_stddev)

    def test_baseline_stddev(self):
        db_conn = Database_Connection()
        stddev = functions.baseline_stddev(self.testfile)
        self.assertIsInstance(stddev, float)

    def test_get_reviews(self):
        db_conn = Database_Connection()
        reviews = functions.get_reviews(db_conn=db_conn, test=True)
        self.assertIsInstance(reviews, list)


if __name__ == '__main__':
    unittest.main()
