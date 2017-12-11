# db.py
import pymysql.cursors


class Database_Connection(object):
    def __init__(self):
        # Connect to the database
        self.connection = pymysql.connect(
                host='localhost',
                user='yelpuser',
                password='password',
                db='yelp_db',
                charset='utf8mb4',
                cursorclass=pymysql.cursors.DictCursor)

    def __del__(self):
        self.connection.close()

    def query(self, sql, args=None):
        with self.connection.cursor() as cursor:
            if args:
                cursor.execute(sql, args)
            else:
                cursor.execute(sql)
        return cursor.fetchall()
