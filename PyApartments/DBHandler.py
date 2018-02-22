import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship

dbname = "apartmentlistings.db"
Base = declarative_base()
import warnings

#I noticed that my address has different listings depending on
#whether I searched by address or by property manager.

#I will collect data as if listings by address and listings by property
#manager were distinct. #I will then associate the address listings with the
#addresses listed for the property managers, if available.

class Property(Base):
    """SQL table to store info on a property manager."""
    __table__ = "Property"
    
    _id = Column(String(36), primary_key=True)
    name = Column(String, nullable=False)
    rating = Column(Integer)
    address = Column(String)
    fees = Column(String)
    city = Column(String)
    state = Column(String(2), nullable=False)
    zipcode = Column(String(5))
    url = Column(String)
    monthlyfees = Column(String)
    onetimefees = Column(String)
    companykey = Column(String)
    accessed = Column(DateTime)


    def __repr__(self):
        return f"<Property(name='{self.name}', city='{self.city}', state='{self.state}')>"

    
class Listing(Base):
    """SQL table to store info on a listing."""
    __tablename__ = "Listing"
    
    _id = Column(String(36), primary_key=True)
    availability = Column(String)
    rentalkey = Column(String)
    model = Column(String)

    propertyid = Column(String, ForeignKey("Property._id"))
    fees = Column(String)
    accessed = Column(DateTime)
    bathroom = Column(Integer)
    bedroom = Column(Integer) #0 corresponds to a studio apartment
    deposit = Column(Integer)
    rent = Column(Integer)
    minrent = Column(Integer)
    maxrent = Column(Integer)
    sqft = Column(Integer)
    

    def __repr__(self):
        return f"<Listing(_id='{self._id}', accessed='{self.accessed}')>"
    

if __name__ == "__main__":
    engine = sqlalchemy.create_engine(f"sqlite:///{dbname}", echo=echo,
                                      encoding="utf-8")
    Base.metadata.create_all(bind=engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    metadata = MetaData()


    #Users will want to look things up based on characteristics, but I
    #just want to check property name, _id.
    propertytable = Table("Property", metadata,
                          Column("_id", String(36), primary_key=True),
                          Column("name", String, nullable=False),
                          Column("rating", Integer),
                          Column("address", String),
                          Column("fees", String),
                          Column("city", String),
                          Column("state", String(2), nullable=False),
                          Column("zipcode", String(5)),
                          Column("url", String),
                          Column("monthlyfees", String),
                          Column("onetimefees", String),
                          Column("companykey", String),
                          Column("accessed", DateTime),
                          Index("idx_propertyname", "name"),
                          Index("idx_property_id", "_id"))
                          
                          
    
    
