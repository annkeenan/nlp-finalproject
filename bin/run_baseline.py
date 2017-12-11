# run_baseline.py
# Calculate the baseline standard deviation/correctness measurements
import argparse
from context import script
from script import functions, db


if __name__ == '__main__':
    db_conn = db.Database_Connection()
    stddev = functions.baseline_stddev(db_conn)
    correctness = functions.baseline_correctness(db_conn)
    print('Baseline:')
    print('stddev\t\t%.5f' % stddev)
    print('correctness\t%.3f' % (correctness*100))
