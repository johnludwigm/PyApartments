

import DBHandler
import sqlite3
from os import makedirs
declarative_base = sqlalchemy.ext.declarative.declarative_base


def createdb(dbname):
    """Creates SQLite database.
    :param dbname: String absolute path of database.
    """
    try:
        connection = sqlite3.connect(dbname)
    except sqlite3.OperationalError as exc:
        print(exc)
        print("Attempting to create necessary directories.")
        makedirs(os.path.dirname(dbname))
        connection=sqlite3.connect(dbname)
    finally:
        connection.close()



def main(dbname="apartmentlistings.db", echo=False, zipcode=None):
    """Intended to access a local database.
    :param dbname: String absolute path to the database, relative path
    by default
    :param zipcode: String ZIP code of desired search area
    """

    createdb(dbname)
    
    engine = sqlalchemy.create_engine(f"sqlite:///{dbname}", echo=echo)
    Base = declarative_base()

    session = makesession(engine)
