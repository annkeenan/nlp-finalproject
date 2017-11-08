# bagofwords.py
from context import script
from script import db, functions
from script.bag_of_words import BagOfWords

bagOfWords = BagOfWords()
bagOfWords.count_words(range_max=1999)

db_conn = db.DatabaseConnection()
reviews = functions.get_reviews(db_conn=db_conn, range_min=2000)
ratings = []
for review in reviews:
    prediction = bagOfWords.predict(review['text'])
    ratings.append({'pred': prediciton,'obsv':review['stars']})

functions.calculate_stddev(ratings)
