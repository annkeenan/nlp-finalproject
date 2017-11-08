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
        sum_squares += math.pow(abs(rating['b'] - rating['r']),2)
    return math.sqrt(sum_squares / (n-1))

def baseline_stddev(db_conn, test=False):
    sql = "SELECT b.stars AS b, r.stars AS r FROM business b JOIN review r ON b.id=r.business_id  WHERE b.review_count>2000"
    if test:
        sql += " LIMIT 2"
    ratings = db_conn.query(sql)
    return calculate_stddev(ratings)
