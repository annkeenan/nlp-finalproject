# functions.py
import math
import re

# Returns a list of the cleaned word(s)
def clean_word(word):
    new_words = []
    words = re.findall(r"[\w'?!\\]+", word)
    for word in words:
        new_word = ''
        for w in range(len(word)):
            # skip escaped words
            if word[w] == '\\':
                w += 1
            # character expressions to keep
            elif word[w] in '?!':
                if new_word:
                    new_words.append(new_word)
                new_words.append(word[w])
                new_word = ''
            # construct the new word
            else:
                new_word += word[w]
        if new_word:
            new_words.append(new_word)
    return new_words

def calculate_stddev(ratings):
    n = len(ratings)
    sum_squares = 0
    for rating in ratings:
        sum_squares += math.pow(abs(rating['pred'] - rating['obsv']),2)
    return math.sqrt(sum_squares / (n-1))

def baseline_stddev(db_conn, test=False):
    sql = "SELECT b.stars AS pred, r.stars AS obsv FROM business b JOIN review r ON b.id=r.business_id  WHERE b.review_count>2000"
    if test:
        sql += " LIMIT 2"
    ratings = db_conn.query(sql)
    return calculate_stddev(ratings)

def get_reviews(db_conn, range_min=None, range_max=None, test=None):
    sql = "SELECT r.text, r.stars FROM review r JOIN business b ON b.id=r.business_id"
    if test:
        sql += " LIMIT 1"
        reviews = db_conn.query(sql)
    elif range_min and range_max:
        sql += " AND b.review_count>=%s AND b.review_count<=%s"
        reviews = db_conn.query(sql,[range_min, range_max])
    elif range_min:
        sql += " AND b.review_count>=%s"
        reviews = db_conn.query(sql,[range_min])
    elif range_max:
        sql += " AND b.review_count<=%s"
        reviews = db_conn.query(sql,[range_max])
    else:
        reviews = db_conn.query(sql)
    return reviews
