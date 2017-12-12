# run_naive_bayes.py
import argparse
from context import script
from script import functions
from script.naive_bayes import BagOfPhrases


if __name__ == '__main__':
    train = 'data/data.train'
    test = 'data/data.test'
    n = 1

    parser = argparse.ArgumentParser()
    parser.add_argument('--train', help='load training data from a file')
    parser.add_argument('--test', help='load testing data from a file')
    parser.add_argument('-n', help='run phrase based naive bayes with N words')
    args = parser.parse_args()

    # Override default files
    if args.train:
        train = args.train
    if args.test:
        test = args.test

    # Construct the model
    if args.n:
        n = int(args.n)

    bagOfWords = BagOfPhrases(n)
    bagOfWords.construct(train)

    # Predict ratings
    ratings = []
    with open(test) as tf:
        for line in tf:
            l = line.rstrip().split(' ')
            prediction = bagOfWords.predict(review=l[1:])
            ratings.append((prediction, int(l[0])))

    # Print results
    stddev = functions.calculate_stddev(ratings)
    correctness = functions.correctness(ratings)
    print('Bag of %d words:' % n)
    print('stddev\t\t%.5f' % stddev)
    print('correctness\t%.3f' % (correctness * 100))
