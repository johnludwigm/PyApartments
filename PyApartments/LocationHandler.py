
import sqlite3

defaults = ("zipcode", "city", "state", "county")

class LocationHandler(object):

    def __init__(self, dbname="location.db"):
        self.connection = sqlite3.connect(dbname)
        self.cursor = self.connection.cursor()


    def getcities(self, **kwargs):
        querypieces = []
        for key, value in filter(lambda x, y: y is not None, kwargs.items()):
            querypieces.append((key, value))
        if querypieces == []:
            raise Exception("No kwargs given.")
        query = f"SELECT city FROM Location WHERE 
        return sorted(tuple(self.execute("SELECT * FROM Location
