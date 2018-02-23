
import datetime
import uuid
from html import unescape

utcnow = datetime.datetime.utcnow


def cleantext(text):
    """Returns stripped, unescaped text."""
    return unescape(text).strip()


def urlextension(zipcode, locationhandler):
    """Returns URL extension for search results on apartments.com.
    :param zipcode: String ZIP code
    """
    zipcode = str(zipcode).zfill(5)
    city, state = locationhandler.getcitystate(zipcode)
    citycomponent = city.lower().replace(" ", "-")
    urlextension = f"{citycomponent}-{state}-{zipcode}/"
    return urlextension


def timestamp():
    """Returns datetime.datetime object, UTC timestamp."""
    return utcnow()


def uuid4():
    """Returns uuid.uuid4 object as string."""
    return str(uuid.uuid4())
