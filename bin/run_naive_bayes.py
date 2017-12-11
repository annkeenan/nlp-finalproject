# bagofwords.py
import argparse
from context import script
from script import functions
from script.naive_bayes import BagOfWords
from script.db import Database_Connection

RANGE_MAX = 1999
RANGE_MIN = 2000

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-r', help='train on a sample size with max range of R')
    parser.add_argument(
        '-t', help='test on a sample size with a min range of T')
    parser.add_argument('train', help='load training data from a file')
    parser.add_argument('test', help='load testing data from a file')
    args = parser.parse_args()

    if args.r:
        RANGE_MAX = args.r
    if args.t:
        RANGE_MIN = args.t

    bagOfWords = BagOfWords()
    bagOfWords.construct(args.trainrange_max=RANGE_MAX)

    ratings = []
    with open(args.test) as tf:
        for line in tf:
            l = line.rstrip().split(' ')
            prediction = bagOfWords.predict(review=l[1:])
            ratings.append({'pred': prediction, 'obsv': review['stars']})
            
    stddev = functions.calculate_stddev(ratings)
    correctness = functions.correctness(ratings)
    print('Bag of words:')
    print('stddev\t\t%.5f' % stddev)
    print('correctness\t%.3f' % (correctness * 100))
