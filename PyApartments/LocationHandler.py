
import sqlite3

defaults = ("zipcode", "city", "state", "county")

class LocationHandler(object):

    def __init__(self, dbname="location.db"):
        self.connection = sqlite3.connect(dbname)
        self.cursor = self.connection.cursor()


    def getcitystate(self, zipcode):
        """Generator yielding (city, stateabbr) tuples.
        :param zipcode: String, ZIP code of desired location
        """
        query = "SELECT city, stateabbr FROM Location WHERE zipcode=?;"
        self.cursor.execute(query, (zipcode, ))
        return self.cursor.fetchone()
