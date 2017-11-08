# test_calculate_stddev.py
import unittest
from context import script
from script import calculate_stddev
from script.db import Database_Connection

class TestBaseline(unittest.TestCase):

    def test_calculate_stddev(self):
        ratings = [
            {'b':5, 'r':4},
            {'b':5, 'r': 3}
        ]
        exp_stddev = 2.2360679775
        stddev = calculate_stddev.calculate_stddev(ratings)
        self.assertAlmostEqual(stddev, exp_stddev)

    def test_baseline_stddev(self):
        db_conn = Database_Connection()
        stddev = calculate_stddev.baseline_stddev(db_conn, True)
        self.assertIsInstance(stddev, float)

if __name__ == '__main__':
    unittest.main()
