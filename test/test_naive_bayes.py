# test_naive_bayes.py
import math
import unittest
from context import script
from script.naive_bayes import BagOfWords

class TestBagOfWords(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestBagOfWords, self).__init__(*args, **kwargs)
        self.bagOfWords = BagOfWords()

    def reset(self):
        self.bagOfWords = BagOfWords()

    def test_construct(self):
        self.reset()
        self.bagOfWords.construct(range_max=1, test=True)
        self.assertIsInstance(self.bagOfWords.get_word_count(), dict)

    def test_process_review(self):
        self.reset()
        word_count = dict()
        reviews = [
            {'stars':5, 'text':'test1 test'},
            {'stars':4, 'text':'test test2'},
            {'stars':2, 'text':'test2 test1'},
            {'stars':4, 'text':'test test1'}
        ]
        exp_word_count = {
            'test':[0,0,0,2,1],
            'test1':[0,1,0,1,1],
            'test2':[0,1,0,1,0],
        }
        for review in reviews:
            self.bagOfWords.process_review(review)
        self.assertEqual(self.bagOfWords.get_word_count(), exp_word_count)

    def test_compile_words(self):
        self.reset()
        words = {
            'test':[0,1,0,0,1],
            'test-test':[1,1,0,0,0]
        }
        exp_words = {
            'test':[2,3,0,0,1]
        }
        self.bagOfWords.compile_words(words)
        self.assertEqual(self.bagOfWords.get_word_count(), exp_words)

    def test_convert_counts(self):
        self.reset()
        words = {
            'test':[0,0,0,0,1]
        }
        exp1 = math.log(.001/1.005, 2)
        exp2 = math.log(1.001/1.005, 2)
        exp_words = {
            'test':[exp1,exp1,exp1,exp1,exp2]
        }
        self.bagOfWords.convert_counts(words)
        self.assertEqual(self.bagOfWords.get_word_count(), exp_words)

    def test_count_words(self):
        self.reset()
        self.bagOfWords.count_words(range_max=1, test=True)
        self.assertIsInstance(self.bagOfWords.get_word_count(), dict)

    def test_predict(self):
        self.reset()
        sentence = 'test test1 test2 test test1'
        word_count = {
            'test':[-10,-10,-10,-10,-1],
            'test1':[-1,-10,-10,-10,-10],
            'test2':[-10,-1,-10,-10,-10],
        }
        # exp_count = [-32,-41,-50,-50,-32] --> 1, 5 --> 1
        exp_prediction = 1
        prediction = self.bagOfWords.predict(sentence, word_count)
        self.assertEqual(prediction, exp_prediction)

if __name__ == '__main__':
    unittest.main()
