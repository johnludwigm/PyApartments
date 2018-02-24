import articlehandler
import commons
import listinghandler
import LocationHandler
import propertyhandler
import requests
from bs4 import BeautifulSoup as BS

baseurl = "https://www.apartments.com/"


listingattrs = {"class": ["rentalGridRow", "hideOnCollapsed", ""]}
class PyApartment(object):
    
    def __init__(self, session=None, sqlsession=None):
        """
        :param session: requests.Session object
        :param sqlsession: sqlalchemy.session object
        """
        if session is None:
            self.session = requests.Session()
        if sqlsession is None:
            raise Exception("No SQLAlchemy.session provided")
        else:
            self.sqlsession = sqlsession
        
        self.locationhandler = LocationHandler.LocationHandler()
        self.searchresultsoup = None


    def executesearch(self, zipcode):
        """Executes search, adds resulting Property and Listing objects
        to sqlsession."""
        for articletag in self.getarticletags(zipcode):
            ah = self.createarticlehandler(articletag)
            propertysoup = BS(self.get(ah.url), "html.parser")
            ph = self.createpropertyhandler(ah, propertysoup)
            self.sqlsession.add(ph.createproperty())
            for tablerowtag in self.gettablerowtags(propertysoup):
                lh = self.createlistinghandler(ph, tablerowtag)
                self.sqlsession.add(lh.createlisting())
            self.sqlsession.commit()


    def getsearchurls(self, zipcode):
        """Generator yielding URLs for apartments.com search results.
        :param zipcode: String ZIP code
        """
        searchurl = baseurl + commons.urlextension(zipcode, self.locationhandler)
        self.searchresultsoup = BS(self.get(searchurl), "html.parser")
        maxpage = getlastpagenum(self.searchresultsoup)
        yield from iterpages(searchurl, lastpagenum=maxpage)

        
    def getarticletags(self, zipcode):
        """Generator yielding article tags when given a zipcode.
        :param zipcode: String ZIP code
        """
        for searchresultsurl in self.getsearchurls(zipcode):
            self.searchresultssoup = BS(self.get(searchresultsurl), "html.parser")
            yield from getproperties(self.searchresultssoup)


    def createarticlehandler(self, articletag):
        """Returns an ArticleHandler."""
        return articlehandler.ArticleHandler(articletag)


    def gettablerowtags(self, propertysoup):
        """Generator yielding tablerow tags.
        :param propertysoup: bs4.BeautifulSoup for the property page
        """
        yield from propertysoup.find_all("tr", attrs=listingattrs)

    
    def createpropertyhandler(self, ArticleHandler, propertysoup):
        """Returns a PropertyHandler object."""
        return propertyhandler.PropertyHandler(ArticleHandler, propertysoup)
    
            
    def createlistinghandler(self, PropertyHandler, tablerowtag):
        """Returns a ListingHandler object."""
        return listinghandler.ListingHandler(PropertyHandler, tablerowtag)

        
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


    def getsoup(self, url):
        """Returns bs4 soup object representing url."""
        return BS(self.get(url), "html.parser")


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
    maxpage = 1
    #Cannot use max(comprehension) because args is sometimes empty
    for tag in filter(lambda tag: tag.has_attr("class"), result):
        if int(tag.get("data-page", 1)) > maxpage:
            maxpage = int(tag.get("data-page", 1))
    return maxpage


def iterpages(url, lastpagenum=1):
    """Generator yielding URLs for all pages in a search result."""
    yield url
    if lastpagenum > 1:
        for num in range(2, lastpagenum + 1):
            yield url + f"{num}/"


searchpropertyattrs = {"class": True, "data-listingid": True, "data-url": True}
def getproperties(searchresultsoup):
    """Generator yielding property article tags from a given search results page."""
    results = iter(searchresultsoup.find_all("article",
                                             attrs=searchpropertyattrs))
    yield from results


if __name__ == "__main__":
    import sqlalchemy
    import os
    p = os.path.abspath("apartmentlistings.db")
    engine = sqlalchemy.create_engine(f"sqlite:///{p}", echo=False)
    Session = sqlalchemy.orm.sessionmaker(bind=engine)
    sqlsession = Session()
    pyapt = PyApartment(sqlsession=sqlsession)
    #pyapt.executesearch("78701")
    l = list(pyapt.getarticletags("78701"))
    ah = pyapt.createarticlehandler(l[0])
    propsoup = BS(pyapt.get(ah.url), "html.parser")
    ph = pyapt.createpropertyhandler(ah, propsoup)
    propitem = ph.createproperty()
    sqlsession.add(propitem)
    sqlsession.commit()
	  
