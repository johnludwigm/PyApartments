import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.orm import sessionmaker, relationship

Base = declarative_base()
import warnings

class Listing(Base):
    """SQL table to store scraped data."""
    __tablename__ = "Listing"

    _id = Column(Integer, primary_key=True)
    #If I discover that Apartments.com assigns unique ids, then I'll change
    #to sequence as below
    #Column(Integer, Sequence('idseq'), primary_key=True)
    accessed = Column(DateTime)

    #Use rent if an exact number is given.
    rent = Column(Integer)
    minprice = Column(Integer)
    maxprice = Column(Integer)
    #Apartments.com is based in the US, so rent is assumed to be in USD ($).
    
    city = Column(String)
    url
    
    rating = Column(Integer)

    def __repr__(self):
        return f"<Listing(_id='{self._id}', )>"
    

def makesession(engine=None):
    """Returns sqlalchemy.Session object."""
    if engine is None:
        warnings.warn("You must later call Session.configure(bind=engine).")
        return sessionmaker()
    return sessionmaker(bind=engine)


def examplequery(session):
    #Returns first row from example query from session.

    #Listing class, not the tablename.
    firstlisting = session.query(Listing).filter_by(city="Austin",
                                                    state="TX").first()
    #firstlisting IS the instance of Listing that we stored to begin with

    #hmm, maybe the listing should be in Dallas
    firstlisting.city = "Dallas"
    #session.dirty returns IdentitySet of items that have been modified, but
    #not yet committed.
    #session.new gives IdentitySet of 
    

def main(dbname):
    """Intended to access a local database.
    :param dbname: String absolute path to the database
    """
    engine = sqlalchemy.create_engine(f"sqlite:///{dbname}", echo=False)

    session = makesession(engine)
    
    new_listing = Listing(_id = 123, rent = 1000)
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

