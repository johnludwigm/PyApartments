import listinghandler
import propertyhandler
import LocationHandler
from bs4 import BeautifulSoup as BS
import commons
import requests
from html import unescape
import re
import uuid
baseurl = "https://www.apartments.com/"


def cleantext(text):
    """Returns stripped, unescaped text."""
    return unescape(text).strip()


def uuid4():
    """Returns uuid.uuid4 object as string."""
    return str(uuid.uuid4())

listingattrs = {"class": ["rentalGridRow", "hideOnCollapsed", ""]}
class PyApartment(object):
    
    def __init__(self, session=None, sqlsession=None):
        """
        :param session: requests.Session object
        :param sqlsession: sqlalchemy.session object
        """
        if session is None:
            self.session = requests.Session()

        self.locationhandler = LocationHandler.LocationHandler()

        self.searchresultsoup = None
        self.propertysoup = None
        

    def getsearchurls(self, zipcode):
        """Generator yielding URLs for apartments.com search results.
        :param zipcode: String ZIP code
        """
        searchurl = baseurl + commons.urlextension(zipcode, self.locationhandler)
        self.searchresultsoup = BS(self.get(searchurl), "html.parser")
        maxpage = getlastpagenum(self.searchresultsoup)
        yield from iterpages(searchurl, lastpagenum=maxpage)

        
    def getsearchresults(self, zipcode):
        """Generator yielding property tags when given a zipcode.
        :param zipcode: String ZIP code
        """
        for searchresultsurl in self.getsearchurls(zipcode):
            self.searchresultssoup = BS(self.get(searchresultsurl), "html.parser")
            yield from getproperties(self.searchresultssoup)


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
        yield from propertysoup.find_all("tr", attrs=listingattrs)


    def createproperty(self, propertysoup=None, **propertykwargs):
        """Returns a Property row object."""
        if propertysoup is None:
            pass
            
    def createlisting(self, tablerowsoup=None, **listingkwargs):
        """Returns a Listing row object."""
        if tablerowsoup is None:
            return 

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
    yield url
    if lastpagenum > 1:
        for num in range(2, lastpagenum + 1):
            yield url + f"{num}/"


searchpropertyattrs = {"class": True, "data-listingid": True, "data-url": True}
def getproperties(searchresultsoup):
    """Generator yielding properties on a given search results page."""
    results = iter(searchresultsoup.find_all("article", attrs=searchpropertyattrs))
    yield from results
