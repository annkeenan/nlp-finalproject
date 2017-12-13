# run_naive_bayes.py
# Run the naive bayes classifier
import argparse
from context import script
import enchant
from script import functions
from script.naive_bayes import BagOfPhrases


if __name__ == '__main__':
    train = 'data/data.train'
    test = 'data/data.test'
    n = 1

    parser = argparse.ArgumentParser()
    parser.add_argument('--train', help='load training data from file TRAIN, default "data/data.train"')
    parser.add_argument('--test', help='load testing data from file TEST, default "data/data.test"')
    parser.add_argument('-n', help='run phrase based naive bayes with N words, default 1')
    parser.add_argument('-s', action='store_true', help='predict sentiment (+/-)')
    parser.add_argument('-p', action='store_true', help='print scores')
    parser.add_argument('-u', action='store_true', help='test user input against the model')
    args = parser.parse_args()

    # Override default files
    if args.train:
        train = args.train
    if args.test:
        test = args.test

    # Construct the model
    if args.n:
        n = int(args.n)

    bagOfPhrases = BagOfPhrases(n)
    bagOfPhrases.construct(train)

    ratings = []
    with open(test) as tf:
        for line in tf:
            l = line.rstrip().split(' ')
            pred_rating = bagOfPhrases.predict(l[1:], args.s)
            obs_rating = int(l[0])
            if args.s:  # predict sentiment
                if obs_rating < 3:
                    ratings.append((pred_rating, 'negative'))
                # elif obs_rating == 3:
                #    ratings.append((pred_rating, 'neutral'))
                else:
                    ratings.append((pred_rating, 'positive'))
            else:  # predict specific star rating
                ratings.append((pred_rating, obs_rating))

    if args.p:
        if args.s:
            print('\nF1 Score:')
            (precision, recall, f1) = functions.f1_score(ratings, args.p)
            print('overall     %.7f    %.7f    %.7f' % (precision, recall, f1))
        else:
            print('\nAccuracy:')
            accuracy = functions.accuracy(ratings, args.p)
            print('all         %.7f' % (accuracy))
            print('\nStandard Deviation:')
            stddev = functions.calculate_stddev(ratings)
            print('%.7f' % stddev)

    # if testing user input
    if args.u:
        print('\nUser Interaction Mode')
        print('Type "quit" to exit.\n')
        Dict = enchant.Dict("en_US")
        while 1:  # loop until user quits the program
            text = input("Input: ")
            if text == 'quit':
                break
            clean_text = functions.clean_review(text, Dict)
            print('%s sentiment\n' % bagOfPhrases.predict(clean_text, True))
