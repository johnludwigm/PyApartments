
import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import (Column, Integer, String, Float,
                        DateTime, ForeignKey, Table, Index)
from sqlalchemy.orm import sessionmaker, relationship

dbname = "apartmentlistings.db"

Base = declarative_base()


#I noticed that my address has different listings depending on
#whether I searched by address or by property manager.

#I will collect data as if listings by address and listings by property
#manager were distinct. #I will then associate the address listings with the
#addresses listed for the property managers, if available.


class Property(Base):
    """SQL table to store info on a property manager."""
    __tablename__ = "Property"
    
    _id = Column(String(36), primary_key=True)
    name = Column(String, nullable=False)
    rating = Column(Integer, default=None)
    address = Column(String, default=None)
    fees = Column(String, default=None)
    city = Column(String, nullable=False)
    state = Column(String(2), nullable=False)
    zipcode = Column(String(5), nullable=False)
    url = Column(String, default=None)
    monthlyfees = Column(String, default=None) 
    onetimefees = Column(String, default=None)
    companykey = Column(String, default=None)
    accessed = Column(DateTime, default=None)
    phone = Column(String(10), default=None)
    description = Column(String, default=None)


    def __repr__(self):
        return f"<Property(name='{self.name}', city='{self.city}', state='{self.state}')>"

    
class Listing(Base):
    """SQL table to store info on a listing."""
    __tablename__ = "Listing"
    
    _id = Column(String(36), primary_key=True)
    availability = Column(String)
    rentalkey = Column(String)
    model = Column(String)
    property_id = Column(String, ForeignKey("Property._id"))
    fees = Column(String)
    accessed = Column(DateTime)
    bathrooms = Column(Integer)
    bedrooms = Column(Integer) #0 corresponds to a studio apartment
    deposit = Column(Integer)
    rent = Column(Integer)
    minrent = Column(Integer)
    maxrent = Column(Integer)
    sqft = Column(Integer)
    

    def __repr__(self):
        return f"<Listing(_id='{self._id}', accessed='{self.accessed}')>"
    

def createdb(dbname, echo=False):
    """Creates the SQLite database using SQLAlchemy.
    :param dbname: string path of database
    :param base: sqlalchemy.ext.declarative.declarative_base instance
    :param echo: sqlalchemy echo parameter
    :param metadata: sqlalchemy.MetaData object
    """
    engine = sqlalchemy.create_engine(f"sqlite:///{dbname}", echo=False,
                                      encoding="utf-8")
    metadata = sqlalchemy.MetaData(bind=engine)
    #It is more efficient to create an index AFTER inserting the
    #initial data (Compare N-many insertions taking n * log(n) time,
    #where n <= N, to one N * log(N) operation).
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
                          Column("phone", String(10)),
                          Column("description", String),
                          Index("idx_propertyname", "name"),
                          Index("idx_property_id", "_id"))
    listingtable = Table("Listing", metadata,
                         Column("_id", String(36), primary_key=True),
                         Column("availability", String),
                         Column("rentalkey", String),
                         Column("model", String),
                         Column("property_id", String,
                                ForeignKey("Property._id")),
                         Column("fees", String),
                         Column("accessed", DateTime),
                         Column("bathrooms", Integer),
                         Column("bedrooms", Integer),
                         Column("deposit", Integer),
                         Column("rent", Integer),
                         Column("minrent", Integer),
                         Column("maxrent", Integer),
                         Column("sqft", Integer),
                         Index("idx_listing_id", "_id"))
    metadata.create_all(engine) 


if __name__ == "__main__":
    createdb(dbname)               
