

import DBHandler
import sqlite3
from os import makedirs
declarative_base = sqlalchemy.ext.declarative.declarative_base

def createdb(dbname, echo=False):
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


def main():
    #Still working out target goals.
    #I will undoubtedly need the following:
    engine = sqlalchemy.create_engine(f"sqlite:///{dbname}", echo=echo)
    Base = declarative_base()
