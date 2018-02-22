import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship

Base = declarative_base()
import warnings

#I noticed that my address has different listings depending on
#whether I searched by address or by property manager.

#I will collect data as if listings by address and listings by property
#manager were distinct. #I will then associate the address listings with the
#addresses listed for the property managers, if available.

class Property(Base):
    """SQL table to store info on property."""
    __table__ = "Property"

    _id = Column(Integer, primary_key=True)
    
    name = Column(String, nullable=False)
    rating = Column(Integer)
    address = Column(String)
    city = Column(String)
    state = Column(String(2), nullable=False)
    zipcode = Column(String(5))
    url = Column(String)
    monthlyfees = Column(String)
    onetimefees = Column(String)

    
class Listing(Base):
    """SQL table to store scraped data."""
    __tablename__ = "Listing"

    _id = Column(String, primary_key=True)
    model = Column(String)
    availability = Column(String)
    propertyid = Column(Integer, ForeignKey("Property._id"))
    fees = Column(String)
    accessed = Column(DateTime)
    bathroom = Column(Integer)
    bedroom = Column(Integer) #0 corresponds to a studio apartment
    deposit = Column(Integer)
    rentalkey = Column(String)
    rent = Column(Integer)
    minprice = Column(Integer)
    maxprice = Column(Integer)
    sqft = Column(Integer)
    

    def __repr__(self):
        return f"<Listing(='{self._id}', )>"
    

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

    session.close()

