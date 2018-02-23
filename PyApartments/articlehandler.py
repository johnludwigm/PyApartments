#######################
#Apply to article tags#
#######################

class ArticleHandler(object):
    __slots__ = ("address", "city", "companykey", "name",
                 "phone", "state", "url", "zipcode")


    def __init__(self, articletag):
        for key, value in getpropertyaddress(articletag).items():
            setattr(self, key, value)
        self.url = getpropertyurl(articletag)
        self.phone = getphonenumber(articletag)
        self.name = getpropertyname(articletag)
        self.companykey = getcompanykey(articletag)
            

urlattrs = {"class": True, "href": True, "title": True}
def getpropertyurl(articletag):
    """Returns string URL for a property."""
    tag = articletag.find("a", attrs=urlattrs)
    try:
        return cleantext(tag["href"])
    except KeyError:
        return None


def getcompanykey(articletag):
    """Returns string companykey."""
    try:
        return articletag["data-ck"]
    except KeyError:
        return None


propertynameattrs = {"itemprop": "name", "content": True}
def getpropertyname(articletag):
    """Return name of the property."""
    tag = articletag.find("meta", attrs=propertynameattrs)
    name = cleantext(tag["content"])
    return name if name != "" else None


addressattrs = {"itemprop": "streetAddress", "content": True}
cityattrs = {"itemprop": "addressLocality", "content": True}
regionattrs = {"itemprop": "addressRegion", "content": True}
zipcodeattrs = {"itemprop": "postalCode", "content": True}
def getpropertyaddress(articletag):
    """Returns dictionary giving full address of the property.
    {"address": address,
     "city": city,
     "state": state,
     "zipcode, zipcode"}
    """
    addresstag = articletag.find("meta", attrs=addressattrs)
    address = cleantext(addresstag["content"])

    citytag = articletag.find("meta", attrs=cityattrs)
    city = cleantext(citytag["content"])
    
    regiontag = articletag.find("meta", attrs=regionattrs)
    state = cleantext(regiontag["content"])

    zipcodetag = articletag.find("meta", attrs=zipcodeattrs)
    zipcode = cleantext(zipcodetag["content"])
    return {"address": address, "city": city,
            "state": state, "zipcode": zipcode}


phoneattrs = {"class": "phone"}
phonepattern = re.compile("\d{3}-\d{3}-\d{4}")
def helper(item):
    return isinstance(item, str) and phonepattern.match(item)


def getphonenumber(articletag):
    """Returns string phone number (apartments.com formats as ddd-ddd-dddd).
    Phone number is returned as 10 digits, no dashes or parentheses...
    """
    phonetag = articletag.find("div", attrs=phoneattrs)
    span = list(filter(helper, phonetag.descendants))
    if span is None:
        return None
    else:
        return cleantext(span[0]).replace("-")
