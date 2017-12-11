# test_naive_bayes.py
import math
import unittest
from context import script
from script.naive_bayes import BagOfWords


class TestBagOfWords(unittest.TestCase):
    testfile = 'data/data.sample'
    bagOfWords = BagOfWords()

    def reset(self):
        self.bagOfWords = BagOfWords()

    def test_convert_counts(self):
        self.reset()
        self.bagOfWords.count_words(self.testfile)
        self.bagOfWords.convert_counts()
        self.assertIsInstance(self.bagOfWords.get_word_count(), dict)

    def test_count_words(self):
        self.reset()
        self.bagOfWords.count_words(self.testfile)
        exp_word_count = {
            'test': [0, 0, 0, 0, 2],
            'tested': [3, 2, 1, 0, 1],
            'testing': [0, 1, 1, 2, 1]
        }
        self.assertEqual(self.bagOfWords.get_word_count(), exp_word_count)

    def test_predict(self):
        self.reset()
        self.bagOfWords.count_words(self.testfile)
        prediction = self.bagOfWords.predict('test')
        self.assertEqual(prediction, 1)


if __name__ == '__main__':
    unittest.main()
