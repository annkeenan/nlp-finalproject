# analyze_data.py
# Analyze the rating composition of a data file
import argparse
from context import script
from collections import Counter


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('data', help='analyze the rating composition of DATA')
    args = parser.parse_args()

    with open(args.data, 'r') as rf:
        ratings = Counter()
        for line in rf:
            l = line.split(' ', 1)
            if len(l) > 1:
                ratings[int(l[0])] += 1
        total_count = sum(ratings.values())
        for rating, count in sorted(ratings.items()):
            print('%s  %f' % (rating, count/total_count))
