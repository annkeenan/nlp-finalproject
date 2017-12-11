# run_baseline.py
# Calculate the baseline standard deviation/correctness measurements
import argparse
from context import script
from script import functions, db


if __name__ == '__main__':
    stddev = functions.baseline_stddev('data/data.test')
    correctness = functions.baseline_correctness('data/data.test')
    print('Baseline:')
    print('stddev\t\t%.5f' % stddev)
    print('correctness\t%.3f' % (correctness*100))
