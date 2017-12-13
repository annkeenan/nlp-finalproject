# test_naive_bayes.py
import math
import unittest
from context import script
from script.naive_bayes import BagOfPhrases


class TestBagOfPhrases(unittest.TestCase):
    testfile = 'data/data.sample'
    bagOfPhrases = BagOfPhrases()

    def reset(self):
        self.bagOfPhrases = BagOfPhrases()

    def test_convert_counts(self):
        self.reset()
        self.bagOfPhrases.count_phrases(self.testfile)
        self.bagOfPhrases.convert_counts()
        exp_phrase_count = {
            ('test',): [0.1/2.5, 0.1/2.5, 0.1/2.5, 0.1/2.5, 2.1/2.5],
            ('tested',): [3.1/7.5, 2.1/7.5, 1.1/7.5, 0.1/7.5, 1.1/7.5],
            ('testing',): [0.1/5.5, 1.1/5.5, 1.1/5.5, 2.1/5.5, 1.1/5.5]
        }
        self.assertEqual(self.bagOfPhrases.get_phrase_count(), exp_phrase_count)

    def test_count_phrases(self):
        self.reset()
        self.bagOfPhrases.count_phrases(self.testfile)
        exp_phrase_count = {
            ('test',): [0, 0, 0, 0, 2],
            ('tested',): [3, 2, 1, 0, 1],
            ('testing',): [0, 1, 1, 2, 1]
        }
        self.assertEqual(self.bagOfPhrases.get_phrase_count(), exp_phrase_count)

    def test_predict(self):
        self.reset()
        self.bagOfPhrases.count_phrases(self.testfile)
        prediction = self.bagOfPhrases.predict('test')
        self.assertEqual(prediction, 1)


if __name__ == '__main__':
    unittest.main()
