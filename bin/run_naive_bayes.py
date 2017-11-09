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
    parser.add_argument('-r', action='store_true', help='train a smaller sample size')
    parser.add_argument('-t', action='store_true', help='test a smaller sample size')
    parser.add_argument('--write', help='save bag of words to a file')
    parser.add_argument('--load', help='load bag of words from a file')
    args = parser.parse_args()

    if args.r:
        RANGE_MAX = 3 # 10=459,626; 30=1,158,861
        TEST = True
    if args.t:
        RANGE_MIN = 6000 # 2 businesses

    bagOfWords = BagOfWords()
    if not args.load:
        bagOfWords.construct(range_max=RANGE_MAX)
        if args.write:
            bagOfWords.save(args.file)
    else:
        bagOfWords.load(args.load)

    db_conn = Database_Connection()
    reviews = functions.get_reviews(db_conn=db_conn, range_min=RANGE_MIN)
    ratings = []
    for review in reviews:
        prediction = bagOfWords.predict(review=review['text'])
        ratings.append({'pred':prediction, 'obsv':review['stars']})


    stddev = functions.calculate_stddev(ratings)
    correctness = functions.correctness(ratings)
    print('Bag of words:')
    print('stddev\t\t%.5f' % stddev)
    print('correctness\t%.3f' % (correctness*100))
