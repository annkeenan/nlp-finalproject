# test_bag_of_words.py
import unittest
from context import script
from script.bag_of_words import BagOfWords

class TestBagOfWords(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestBagOfWords, self).__init__(*args, **kwargs)
        self.bagOfWords = BagOfWords()

    def reset(self):
        self.bagOfWords = BagOfWords()

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

    def test_count_words(self):
        self.reset()
        self.bagOfWords.count_words(range_max=1, test=True)
        self.assertIsInstance(self.bagOfWords.get_word_count(), dict)

    def test_predict(self):
        self.reset()
        sentence = 'test test1 test2 test test1'
        word_count = {
            'test':[0,1,0,0,5],
            'test1':[10,0,0,0,0],
            'test2':[0,1,0,0,0],
        }
        # exp_count = [20,3,0,0,10] --> 76/33
        exp_prediction = 2.30303030303
        prediction = self.bagOfWords.predict(sentence, word_count)
        self.assertAlmostEqual(prediction, exp_prediction)

if __name__ == '__main__':
    unittest.main()
