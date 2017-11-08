# calculate_stddev.py
import math
from script.db import Database_Connection

def calculate_stddev(ratings):
    n = len(ratings)
    sum_squares = 0
    for rating in ratings:
        sum_squares += math.pow(abs(rating['b'] - rating['r']),2)
    return math.sqrt(sum_squares / (n-1))

def baseline_stddev(db_conn, test=False):
    sql = "SELECT b.stars AS b, r.stars AS r FROM business b JOIN review r ON b.id=r.business_id  WHERE b.review_count>2000"
    if test:
        sql += " LIMIT 2"
    ratings = db_conn.query(sql)
    return calculate_stddev(ratings)
