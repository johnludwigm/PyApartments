
from bs4 import BeautifulSoup as BS
import requests

descriptors = ("bathrooms",
               "bedrooms", 
               "city",
               "maxprice",
               "minprice",
               "state")

baseURL = "https://www.apartments.com/"
def formatURL(**kwargs):
    """Formats a URL extension for apartments.com queries.
    kwargs:
    bathrooms: Integer number of bathrooms (1 - 3, 3 includes 4, 5, 6...)
    bedrooms: int/string number of bedrooms ("studio", 1 - 4, 4 includes 5, 6, 7...)
    city: String city name
    """
    if "state" not in kwargs:
        raise NoStateException("Please provide a state in the USA.")
    
    specs = {key: kwargs.get(key, default=None) for key in descriptors}
    
    
    
    
class PyApartment(object):
    
    austin-tx/695-to-1500/