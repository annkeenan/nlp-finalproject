# run_baseline.py
# Calculate the baseline standard deviation/accuracy measurements
import argparse
from context import script
from script import functions, db


if __name__ == '__main__':
    print('Baseline:')

    print('\nStar rating:')
    stddev = functions.baseline_stddev('data/data.test')
    accuracy = functions.baseline_accuracy('data/data.test')
    print('stddev     %.5f' % stddev)
    print('accuracy   %.5f' % (accuracy*100))
