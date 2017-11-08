# baseline
from context import script
from script import functions, db

db_conn = db.Database_Connection()
stddev = functions.baseline_stddev(db_conn)
print('Baseline stddev = %.5f' % stddev)
