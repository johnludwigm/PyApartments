#import DBHandler
import LocationHandler
from bs4 import BeautifulSoup as BS
import datecommons
import requests
from html import unescape
import re

def cleantext(text):
    """Returns stripped, unescaped text."""
    return unescape(text).strip()


baseURL = "https://www.apartments.com/"

class PyApartment(object):
    
    def __init__(self, url=None, session=None):
        if session is None:
            self.session = requests.Session()

        self.locationhandler = LocationHandler.LocationHandler()

        self.searchresultsoup = None
        self.propertysoup = None
        
        if url is not None:
            self.searchresultsoup = BS(self.get(url), "html.parser")
        else:
            self.searchresultsoup = None
        
        
    def getsearchresults(self, zipcode):
        """Yields search results (properties, not property pages)
        when given a zipcode.
        :param zipcode:
        """
        zipcode = str(zipcode).zfill(5)
        city, state = self.locationhandler.getcitystate(zipcode)
        citycomponent = city.lower().replace(" ", "-")
        urlextension = f"{citycomponent}-{state}-{zipcode}/"
        searchurl = baseURL + urlextension
        self.soup = BS(self.get(searchurl), "html.parser")
        if self.soup is None:
            raise Exception(f"Trouble with ZIP code: {zipcode}, {city}, {state}")             


    def get(self, url, html=True, content=False):
        """Handles self.session and returns data from desired URL."""
        if html and content:
            raise Exception("Either HTML text OR content may be returned.")
        try:
            result = self.session.get(url)
        except Exception as exc:
            print(exc)
            self.session = requests.Session()
            try:
                result = self.session.get(url)
            except:
                raise Exception("Cannot resolve requests.Session object.")
        if html:
            return result.text
        else:
            return result.content


    def getpropertyinfo(self, propertysoup, timestamp=True):
        """Returns property information given a property page.
        :param timestamp: Boolean, if True, then the property information
        will be updated with current information and timestamped.
        """
        
        propertyname = getpropertyname(soup)
        address = getpropertyaddress(soup)
        
        getallfees(propertysoup)
        getpropertydescription(soup)
        if timestamp:
            accesstime = datecommons.utcstamp()
        

    def getlistings(self, propertysoup, propertytable):
        """Generator yielding SQLAlchemy Listing objects.
        :param propertysoup: bs4.BeautifulSoup for the property page
        :param propertytable: SQLAlchemy Property record.
        """
        yield from soup.find_all("tr", attrs={"class":
                                              ["rentalGridRow",
                                               "hideOnCollapsed",
                                               ""]})


#######################################
#Apply to the results page of a search#
#######################################
def getlastpagenum(searchresultsoup):
    """Gets last page from results."""
    #The footer of the results page lists pages containing at most 25
    #results each. So at the bottom of the landing page for a search that
    #would get 126 results, it would say <1 2 3 ... 6>. 25 results on each
    #of pages 1 (current), 2, 3, 4, and 5, but 1 result on page 6.

    result = searchresultsoup.select("li div a")    
    return max(int(tag["data-page"]) for tag in result
               if not tag.has_attr("class"))


def iterpages(url, lastpagenum=1):
    """Generator yielding URLs for all pages in a search result."""
    if lastpagenum == 1:
        yield url
    else:
        for num in range(2, lastpagenum + 1):
            yield url + f"{num}/"


searchpropertyattrs = {"class": True, "data-listingid": True, "data-url": True}
def getproperties(searchresultsoup):
    """Generator yielding properties on a given search results page."""
    results = searchresultsoup.find_all("article", attrs=searchpropertyattrs)
    yield from results

                     
#########################
#Apply to property pages#
#########################
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
            description = cleantext(next(iterfees).text)
            price = cleantext(next(iterfees).text)
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
        return cleantext(descriptiontag.text)
    return None

    
#######################
#Apply to article tags#
#######################
urlattrs = {"class": True, "href": True, "title": True}
def getpropertyurl(articletag):
    """Returns string URL for a property."""
    tag = articletag.find("a", attrs=urlattrs)
    return cleantext(tag["href"])


def getcompanykey(articletag):
    """Returns string companykey."""
    return articletag["data-ck"]

    
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
    """Returns string phone number (apartments.com formats as ddd-ddd-dddd)."""
    phonetag = articletag.find("div", attrs=phoneattrs)
    span = list(filter(helper, phonetag.descendants))
    if span is None:
        return None
    else:
        return cleantext(span[0])
