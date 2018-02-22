
import os
import sqlalchemy


def createdb(dbname, echo=echo):
    """Creates the SQLite database using SQLAlchemy.
    :param dbname: string path of database
    :param base: sqlalchemy.ext.declarative.declarative_base instance
    :param echo: sqlalchemy echo parameter
    :param metadata: sqlalchemy.MetaData object
    """
    engine = sqlalchemy.create_engine(dbname, echo=echo)
    Base = sqlalchemy.ext.declarative.declarative_base()
    

    #It is more efficient to create an index AFTER you've inserted
    #the initial data.

def main(dbname="apartmentlistings.db", echo=False, zipcode=None):
    """Intended to access a local database.
    :param dbname: String absolute path to the database, relative path
    by default
    :param zipcode: String ZIP code of desired search area
    """
    if zipcode is None:
        return
    
    if not os.path.exists(dbname):
        createdb(os.path.abspath(dbname))
    
    Base = declarative_base()

    session = makesession(engine)

    session.close()


def makesession(engine=None):
    """Returns sqlalchemy.Session object."""
    if engine is None:
        warnings.warn("You must later call Session.configure(bind=engine).")
        return sessionmaker()
    return sessionmaker(bind=engine)


irstlisting = session.query(Listing).filter_by(city="Austin",
                                                    state="TX").first()

    

def main(dbname):
    session.add(new_listing)
    #the transaction is pending, nothing has been done to the database yet.
    #session.add_all(#iterable of objects)
    session.commit()

    session.query(User).filter(User.name.in_(['Edwardo', 'fakeuser'])).all()
    session.rollback()
    for listing in session.query(Listing).order_by(Listing.city):
        print(listing.state)

    for listing in session.query(Listing.state, Listing.city).order_by(Listing.city):
        print(listing.state)

    session.close()
