
import datetime

utcnow = datetime.datetime.utcnow
isoformat = datetime.datetime.isoformat

def utcstamp():
    """Returns string UTC-formatted timestamp."""
    return isoformat(utcnow())


def urlextension(zipcode, locationhandler):
    """Returns URL extension for search results on apartments.com.
    :param zipcode: String ZIP code
    """
    zipcode = str(zipcode).zfill(5)
    city, state = locationhandler.getcitystate(zipcode)
    citycomponent = city.lower().replace(" ", "-")
    urlextension = f"{citycomponent}-{state}-{zipcode}/"
    return urlextension
