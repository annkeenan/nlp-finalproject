# run_process_db.py
import argparse
from context import script
from script import functions


if __name__ == '__main__':
    range_min = None
    range_max = None
    parser = argparse.ArgumentParser()
    parser.add_argument('--min', help='test on a sample size with a min range of MIN')
    parser.add_argument('--max', help='train on a sample size with max range of MAX')
    parser.add_argument('write', help='save bag of words to a file')
    args = parser.parse_args()

    if args.min:
        range_min = args.min
    if args.max:
        range_max = args.max

    functions.process_db(args.write, range_min, range_max)
