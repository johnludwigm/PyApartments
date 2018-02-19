from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Listing(Base):
    """SQL table to store scraped data."""
    __tablename__ = "Listing"
    
    
    
    

def main(dbname):
    engine = create_engine(f"sqlite:///{dbname}", echo=False)
    