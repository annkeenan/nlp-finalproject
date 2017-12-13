# functions.py
# Helper functions for cleaning reviews and calculating accuracy
import math
import re
import enchant
from collections import defaultdict
from script.db import Database_Connection

START = '<s>'
STOP = '</s>'


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


# Calculate F1 score of sentiment analysis
def f1_score(ratings, output=False):
    tp = defaultdict(int)  # true positive
    fn = defaultdict(int)  # false negative
    fp = defaultdict(int)  # false positive
    for (pred, obs) in ratings:
        if pred == obs:
            tp[obs] += 1
        else:
            fn[obs] += 1
            fp[pred] += 1

    prec = defaultdict(float)
    rec = defaultdict(float)
    f1 = defaultdict(float)
    if output:
        print('key         precision    recall       F1 score')
        print('-'*47)
    for s in tp.keys():
        prec[s] = tp[s]/(tp[s]+fp[s])
        rec[s] = tp[s]/(tp[s]+fn[s])
        f1[s] = 2 / (1 / prec[s] + 1 / rec[s])
        if output:
            print('%-10s  %.7f    %.7f    %.7f' % (s, prec[s], rec[s], f1[s]))
    overall_prec = sum(prec.values())/len(prec)
    overall_rec = sum(rec.values())/len(rec)
    overall_f1 = sum(f1.values())/len(f1)
    return (overall_prec, overall_rec, overall_f1)


# Check the accuracy (recall) of the predicted review comparing the tuple pair (obs, pred)
def accuracy(ratings, output=False):
    correct = defaultdict(int)
    total = defaultdict(int)
    for (pred, obs) in ratings:
        if pred == obs:
            correct[obs] += 1
        total[obs] += 1
    if output:
        print('rating      accuracy')
        print('-'*21)
        for s in correct.keys():
            print('%-10s  %.7f' % (str(s), correct[s]/total[s]))
    return sum(correct.values()) / sum(total.values())


# Calculate the baseline accuracy
def baseline_accuracy(filename):
    correct = 0
    n = 0
    with open(filename, 'r') as rf:
        for line in rf:
            l = line.split(' ', 1)
            if int(l[0]) == 3:
                correct += 1
            n += 1
    return correct/n


# Calculate the standard deviation of a list of predicted and observed ratings
def calculate_stddev(ratings):
    n = len(ratings)
    sum_squares = 0
    for (pred, obs) in ratings:
        sum_squares += math.pow(pred - obs, 2)
    return math.sqrt(sum_squares / (n - 1))


# Calculate the baseline standard deviation
def baseline_stddev(filename):
    sum_squares = 0
    n = 0
    with open(filename, 'r') as rf:
        for line in rf:
            l = line.split(' ', 1)
            sum_squares += math.pow(int(l[0]) - 3, 2)
            n += 1
    return math.sqrt(sum_squares / (n - 1))


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
        sql += " WHERE b.review_count>=%s"  # AND b.stars=3"
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
