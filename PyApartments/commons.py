
import datetime

utcnow = datetime.datetime.utcnow
isofomrat = datetime.datetime.isoformat

def utcstamp():
    """Returns string UTC-formatted timestamp."""
    return isofomrat(utcnow())


def formaturl(zipcode):
    """Returns URL extension for search results on apartments.com.
    :param zipcode: String ZIP code
    """
    zipcode = str(zipcode).zfill(5)
    city, state = self.locationhandler.getcitystate(zipcode)
    citycomponent = city.lower().replace(" ", "-")
    urlextension = f"{citycomponent}-{state}-{zipcode}/"
    return urlextension
