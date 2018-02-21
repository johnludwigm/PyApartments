import DBHandler
from bs4 import BeautifulSoup as BS
import requests
from html import unescape

def cleantext(text):
    """Returns stripped, unescaped text."""
    return unescape(text).strip()


baseURL = "https://www.apartments.com/"
descriptors = ("bathrooms",
               "bedrooms", 
               "city",
               "maxprice",
               "minprice",
               "state")


class PyApartment(object):
    
    def __init__(self, url=None, session=None):
        if self.session is None:
            self.session = requests.Session()

        self.soup = self.get(url)
            
    def getlistings(self, **kwargs):
        """Get listings given specifications.
        :param bathrooms: Integer number of bathrooms (1 - 3; 3 = 3+)
        :param bedrooms: Integer or String, number of bedrooms
        ("studio" or 1 - 4; 4 = 4+)
        :param city: String city name
        :param maxprice: Integer max price
        :param minprice: Integer min price
        :param state: String state abbreviation ("TX" good, "Texas" bad)
        """
        self.soup = BS(self.get(url), "html.parser")
        if self.soup is None:
            return None
               


    def get(self, url, html=True, content=False):
        """Handles self.session and returns data from desired URL."""
        if text and content:
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
        
        prop = getpropertyname(soup)
        # get the address of the property
    getpropertyaddress(soup)
    # get the size of the property
    get_property_size(soup)
    getallfees(propertysoup)
    # get the images as a list
    #get_images(soup)
    getpropertydescription(soup)
    # only look in this section (other sections are for example for printing)
    soup = soup.find('section', class_='specGroup js-specGroup')
    get_pet_policy(soup, fields)
    # get parking information
    get_parking_info(soup, fields)
    # get the 'property information'
    get_features_and_info(soup)


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

def getlastpagenum(resultsoup):
    """Gets last page from results."""
    #The footer of the results page lists pages containing at most 25
    #results each. So at the bottom of the landing page for a search that
    #would get 126 results, it would say <1 2 3 ... 6>. 25 results on each
    #of pages 1 (current), 2, 3, 4, and 5, but 1 result on page 6.

    result = soup.select("li div a")    
    return max(int(tag["data-page"]) for tag in result
               if not tag.has_attr("class"))


def iterpages(url, lastpagenum=1):
    """Generator yielding URLs for all pages in a search result."""
    if lastpagenum == 1:
        yield url
    else:
        for num in range(2, lastpagenum + 1):
            yield url + f"{num}/"


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
    monthlyfees_tag = propertysoup.find("div", attrs=monthlyfeestag)

    return {"onetimefees": getfees(onetimefees_tag),
            "monthlyfees": getfees(monthlyfees_tag)}


descriptionattrs = {"itemprop": "description"}
def getpropertydescription(propertysoup):
    """Get the description for the property."""
    descriptiontag = propertysoup.find("p", attrs=descriptionattrs)
    if descriptiontag is not None:
        return cleantext(descriptiontag.text)
    return None


def get_property_size(soup):
    """Get the property size of the first one bedroom."""
    #note: this might be wrong if there are multiple matches!!!
    fields['size'] = ''    
    obj = soup.find('tr', {'data-beds': '1'})
    if obj is not None:
        data = obj.find('td', class_='sqft').getText()
        data = prettify_text(data)
        fields['size'] = data


#######################
#Apply to article tags#
#######################
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
            "state": state, "zipcode, zipcode"}


urlattrs = {"class": True, "href": True, "title": True}
def getpropertyurl(articletag):
    tag = articletag.find("a", attrs=urlattrs)
    return cleantext(tag["href"])


phoneattrs = {"class": "phone"}
def getphonenumber(articletag):
    """Returns string phone number (apartments.com formats as ddd-ddd-dddd)."""
    phonetag = articletag.find("div", attrs=phoneattrs)
    span = list(phonetag.descendants)
    if span == []:
        return None
    else:
        return cleantext(span[0].text)
        
        
def getlastpagenum(searchresultsoup):
    """Gets last page from results."""
    #The footer of the results page lists pages containing at most 25
    #results each. So at the bottom of the landing page for a search that
    #would get 126 results, it would say <1 2 3 ... 6>. 25 results on each
    #of pages 1 (current), 2, 3, 4, and 5, but 1 result on page 6.

    result = soup.select("li div a")    
    return max(int(tag["data-page"]) for tag in result
               if not tag.has_attr("class"))
