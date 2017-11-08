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

if __name__ == '__main__':
    unittest.main()
