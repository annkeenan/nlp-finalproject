# functions.py
import math
import re
import enchant
from script.db import Database_Connection


# Returns a list of words from the cleaned review
def clean_review(review, Dict):
    new_words = []
    words = re.findall(r"[\w'\\]+", review.lower())
    for word in words:
        new_word = ''
        for w in range(len(word)):
            # skip escaped words
            if word[w] == '\\' or \
                    (word[w] == '\'' and (w == 0 or w == (len(word) - 1))):
                w += 1
            # construct the new word
            else:
                new_word += word[w]
        if new_word and Dict.check(new_word):
            new_words.append(new_word)
    return new_words


# Check the correctness of the predicted review
def correctness(ratings):
    n = len(ratings)
    correct = 0
    for rating in ratings:
        if rating['pred'] == rating['obsv']:
            correct += 1
    return correct / n


# Calculate the baseline
def baseline_correctness(db_conn, test=False):
    sql = "SELECT b.stars AS pred, r.stars AS obsv FROM business b JOIN review r ON b.id=r.business_id  WHERE b.review_count>=2000 AND b.stars=3"
    if test:
        sql += " LIMIT 5"
    ratings = db_conn.query(sql)
    for rating in ratings:
        rating['pred'] = math.ceil(rating['pred'])
    return correctness(ratings)


# Calculate the standard deviation of a list of predicted and observed ratings
def calculate_stddev(ratings):
    n = len(ratings)
    sum_squares = 0
    for rating in ratings:
        sum_squares += math.pow(abs(rating['pred'] - rating['obsv']), 2)
    return math.sqrt(sum_squares / (n - 1))


# Calculate the baseline standard deviation
def baseline_stddev(db_conn, test=False):
    sql = "SELECT b.stars AS pred, r.stars AS obsv FROM business b JOIN review r ON b.id=r.business_id WHERE b.review_count>2000 AND b.stars=3"
    if test:
        sql += " LIMIT 5"
    ratings = db_conn.query(sql)
    return calculate_stddev(ratings)


# Query the database for a list of reviews/associated star ratings
def get_reviews(db_conn, range_min=None, range_max=None, test=None):
    sql = "SELECT r.text, r.stars FROM review r JOIN business b ON b.id=r.business_id"
    if test:
        sql += " LIMIT 5"
        reviews = db_conn.query(sql)
    elif range_min and range_max:
        sql += " WHERE b.review_count>=%s AND b.review_count<=%s"
        reviews = db_conn.query(sql, [range_min, range_max])
    elif range_min:
        sql += " WHERE b.review_count>=%s AND b.stars=3"
        reviews = db_conn.query(sql, [range_min])
    elif range_max:
        sql += " WHERE b.review_count<=%s"
        reviews = db_conn.query(sql, [range_max])
    else:
        reviews = db_conn.query(sql)
    return reviews


# Process the database reviews and output to a file
def process_db(filename, range_min=0, range_max=3):
    Dict = enchant.Dict("en_US")
    db_conn = Database_Connection()
    reviews = get_reviews(db_conn, range_min, range_max)
    with open(filename, 'w') as f:
        for review in reviews:
            f.write('%d' % review['stars'])
            for word in clean_review(review['text'], Dict):
                f.write(' %s' % word)
            f.write('\n')
