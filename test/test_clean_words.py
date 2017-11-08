# test_clean_words.py
import unittest
from context import script
from script import clean_words

class TestCleanWords(unittest.TestCase):

    def test_clean_word(self):
        words = ['test?','test":;','test\'s','test-test','test\n']
        exp_words = [['test','?'],['test'],['test\'s'],['test','test'],['test']]
        for w in range(len(words)):
            new_word = clean_words.clean_word(words[w])
            self.assertEqual(new_word, exp_words[w])

    def test_compile_words(self):
        words = {
            'test':[0,1,0,0,1],
            'test-test':[1,1,0,0,0]
        }
        exp_words = {
            'test':[2,3,0,0,1]
        }
        new_words = clean_words.compile_words(words)
        self.assertEqual(new_words, exp_words)
        pass

if __name__ == '__main__':
    unittest.main()
