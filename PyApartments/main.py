
import os
import PyApartment
import sqlalchemy


def main(dbname="apartmentlistings.db", echo=False, zipcode=None):
    """Intended to access a local database.
    :param dbname: String absolute path to the database, relative path
    by default
    :param zipcode: String ZIP code of desired search area
    """
    if zipcode is None:
        return

    engine = sqlalchemy.create_engine(f"sqlite:///{dbname}", echo=False)
    Session = sqlalchemy.orm.sessionmaker(bind=engine)
    session = Session()
    pyapt = PyApartment.PyApartment(sqlsession=session)
    pyapt.executesearch(zipcode)
    session.commit()
    session.close()


if __name__ == "__main__":
    zipcode = input("Enter zipcode: ")
    main(zipcode=zipcode)
