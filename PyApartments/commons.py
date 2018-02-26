
import datetime
from hashlib import md5
from html import unescape
import uuid
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


def hashmd5(args):
    hashobj = md5()
    for arg in filter(None, args):
        hashobj.update(str(arg).encode())
    return hashobj.hexdigest()

def timestamp():
    """Returns datetime.datetime object, UTC timestamp."""
    return utcnow()


def uuid4():
    """Returns uuid.uuid4 object as string."""
    return str(uuid.uuid4())
