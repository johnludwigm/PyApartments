
import datetime

utcnow = datetime.datetime.utcnow
isofmrat = datetime.datetime.isoformat

def utcstamp():
    """Returns string UTC-formatted timestamp."""
    return isofmrat(utcnow())
