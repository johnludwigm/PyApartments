
import datetime

utcnow = datetime.datetime.utcnow
isofomrat = datetime.datetime.isoformat

def utcstamp():
    """Returns string UTC-formatted timestamp."""
    return isofomrat(utcnow())
