# test_functions.py
import unittest
from context import script
from script import functions
from script.db import Database_Connection

class TestFunctions(unittest.TestCase):

    def test_clean_word(self):
        words = ['test?','test":;','test\'s','test-test','test\n']
        exp_words = [['test','?'],['test'],['test\'s'],['test','test'],['test']]
        for w in range(len(words)):
            new_word = functions.clean_word(words[w])
            self.assertEqual(new_word, exp_words[w])

    def test_calculate_stddev(self):
        ratings = [
            {'b':5, 'r':4},
            {'b':5, 'r': 3}
        ]
        exp_stddev = 2.2360679775
        stddev = functions.calculate_stddev(ratings)
        self.assertAlmostEqual(stddev, exp_stddev)

    def test_baseline_stddev(self):
        db_conn = Database_Connection()
        stddev = functions.baseline_stddev(db_conn, True)
        self.assertIsInstance(stddev, float)

if __name__ == '__main__':
    unittest.main()
