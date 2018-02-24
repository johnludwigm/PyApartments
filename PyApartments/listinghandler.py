#################################
#Apply to individual listings in#
# the table on a property page. #
#################################
import re
import commons
import DBHandler


class ListingHandler(object):
    __slots__ = ("_id", "accessed", "availability", "bathrooms", "bedrooms",
                 "deposit",
                 #"fees",
                 "maxrent", "minrent", "model",
                 "rent", "rentalkey", "property_id", "sqft")

    def __init__(self, PropertyHandler, tablerowtag):
        properties = getdata(tablerowtag)
        for key in self.__slots__:
            setattr(self, key, properties.get(key, None))
        self.property_id = PropertyHandler._id       


    def createlisting(self):
        """Returns Listing object for SQLAlchemy."""
        if self._id is None:
            self._id = commons.uuid4()
        self.accessed = commons.timestamp()
        return DBHandler.Listing(**{key: getattr(self, key, None)
                                    for key in self.__slots__})


numberpattern = re.compile("[\d,]+")
def resolvenumbers(text):
    """Returns tuple of integers in the text.
    :param text: string that begins and ends with a number
    e.g. text='1,201 - 1203', '22,301'
    Resolves problem of numbers given as either "\d+" or "\d+ - \d+".
    """
    try:
        return [int(strnum.replace(",", "")) for strnum in
                numberpattern.findall(text.strip())]
    except ValueError:
        return [None]


rentattrs = {"class": "rent"}
def getrent(tablerowtag):
    """Returns list of rent prices.
    If rent for a listing is given as a range (minrent - maxrent),
    returns [(int) minprice, (int) maxprice].
    
    Otherwise, returns [(int) rent].
    """
    renttag = tablerowtag.find("td", attrs=rentattrs)
    if renttag is None:
        return [None]
    return resolvenumbers(renttag.text.strip("$ "))
    

sqftattrs = {"class": "sqft"}
def getsqft(tablerowtag):
    """Returns int number of square feet for listing."""
    sqfttag = tablerowtag.find("td", attrs=sqftattrs)
    content = sqfttag.text
    if not content:
        return [None]
    return resolvenumbers(content.strip("Sq Ft"))


availableattrs = {"class": "available"}
def getavailability(tablerowtag):
    """Returns string availability status of listing."""
    availabletag =  tablerowtag.find("td", attrs=availableattrs)
    return availabletag.text.strip()


depositattrs = {"class": ["deposit", ""]}
def getdeposit(tablerowtag):
    """Returns integer deposit."""
    deposittag = tablerowtag.find("td", attrs=depositattrs)
    return resolvenumbers(deposittag.text.strip(" $"))[0]



unitattrs = {"class": "unit"}
def getunit(tablerowtag):
    """Returns string identifying the listed unit."""
    unittag = tablerowtag.find("td", attrs=unitattrs)
    returnstr = unittag.text.strip()
    return returnstr if returnstr != "" else None


def getdata(tablerowtag):
    """Returns dictionary:
    :param tablerowtag: tablerow <tr> tag in listing table
    on the property page

    Returns dictionary:
    {availability: str,
     accessed: datetime.datetime,
     bathrooms: int,
     bedrooms: int,
     deposit: int,
     maxrent: int,
     minrent: int,
     model: str,
     rentalkey: str,
     rent: int,
     sqft, int,
     unit: str}     
    """
    returndict = {"bathrooms": tablerowtag["data-baths"].strip(),
                  "bedrooms": int(tablerowtag["data-beds"]),
                  "model": tablerowtag["data-model"],
                  "rentalkey": tablerowtag["data-rentalkey"]}

    
    #maxrent = tablerowtag["data-maxrent"]
    rent = getrent(tablerowtag)
    if len(rent) == 2:
        returndict["minrent"], returndict["maxrent"] = rent
    elif len(rent) == 1:
        returndict["rent"] = rent[0]
    else:
        returndict["rent"] = None

    returndict["sqft"] = getsqft(tablerowtag)[0]
    returndict["availability"] = getavailability(tablerowtag)
    returndict["unit"] = getunit(tablerowtag)
    returndict["deposit"] = getdeposit(tablerowtag)
    return returndict
