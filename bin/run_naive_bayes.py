# run_naive_bayes.py
import argparse
from context import script
from script import functions
from script.naive_bayes import BagOfWords, BagOfPhrases


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('train', help='load training data from a file')
    parser.add_argument('test', help='load testing data from a file')
    parser.add_argument('-p', action='store_true', help='run phrase based naive bayes')
    args = parser.parse_args()

    bagOfWords = BagOfWords()
    if args.p:
        bagOfWords = BagOfPhrases()
    bagOfWords.construct(args.train)

    ratings = []
    with open(args.test) as tf:
        for line in tf:
            l = line.rstrip().split(' ')
            prediction = bagOfWords.predict(review=l[1:])
            ratings.append((prediction, int(l[0])))

    stddev = functions.calculate_stddev(ratings)
    correctness = functions.correctness(ratings)
    if args.p:
        print('Bag of phrases:')
    else:
        print('Bag of words:')
    print('stddev\t\t%.5f' % stddev)
    print('correctness\t%.3f' % (correctness * 100))
