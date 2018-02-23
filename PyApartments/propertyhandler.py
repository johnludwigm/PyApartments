#########################
#Apply to property pages#
#########################
import commons
import DBHandler

class PropertyHandler(object):
    __slots__ = ("_id", "accessed", "address", "city", "companykey",
                 "description", "fees", "monthlyfees", "name", "onetimefees",
                 "phone", "rating", "state", "url", "zipcode")
    

    def __init__(self, ArticleHandler, propertysoup, _id=None):
        self._id = _id
        for key in ArticleHandler.__slots__:
            setattr(self, key, getattr(ArticleHandler, key, None))
        
        self.fees = getallfees(propertysoup)
        self.description = getpropertydescription(propertysoup)
        

    def createproperty(self):
        """Returns Property object for SQLAlchemy."""
        if self._id is None:
            self._id = commons.uuid4()
        self.accessed = commons.timestamp()
        return DBHandler.Property(**{key: getattr(self, key, None)
                                     for key in self.__slots__})

    
onetimefeesattrs = {"class": "oneTimeFees"}
monthlyfeesattrs = {"class": "monthlyFees"}
feeattr = {"class": "descriptionWrapper"}
def getfees(fees_tag):
    """Returns string detailing fees."""
    if fees_tag is None:
        return None
    individualfees = fees_tag.find_all("span")
    if len(individualfees) % 2 == 1:
        #We expect that the span tags alternate between a description
        #of a fee and the amount of the fee. So an odd number of span tags
        #is unexpected.
        return None
    fees = []
    iterfees = iter(individualfees)
    while True:
        try:
            description = commons.cleantext(next(iterfees).text)
            price = commons.cleantext(next(iterfees).text)
            fees.append(f"{description}: {price}")
        except StopIteration:
            break
    return ", ".join(fees)


def getallfees(propertysoup):
    """Returns dictionary of one time fees and monthly fees."""
    onetimefees_tag = propertysoup.find('div', attrs=onetimefeesattrs)       
    monthlyfees_tag = propertysoup.find("div", attrs=monthlyfeesattrs)
    return {"onetimefees": getfees(onetimefees_tag),
            "monthlyfees": getfees(monthlyfees_tag)}


descriptionattrs = {"itemprop": "description"}
def getpropertydescription(propertysoup):
    """Get the description for the property."""
    descriptiontag = propertysoup.find("p", attrs=descriptionattrs)
    if descriptiontag is not None:
        return commons.cleantext(descriptiontag.text)
    return None
