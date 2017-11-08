# word_count.py
from script.db import Database_Connection

def process_review(word_count, review):
    for word in review['text'].split(' '):
        if word not in word_count:
            word_count[word] = [0] * 5
        word_count[word][review['stars']-1] += 1

def count_words(db_conn, range_min=None, range_max=None):
    word_count = dict()
    sql = "SELECT r.text, r.stars FROM review r JOIN business b ON b.id=r.business_id"
    if range_min and range_max:
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
    for review in reviews:
        process_review(word_count, review)
    return word_count
