
from bs4 import BeautifulSoup as BS
import requests
from html import unescape

def cleantext(text):
    """Returns stripped, unescaped text."""
    return unescape(text).strip()

descriptors = ("bathrooms",
               "bedrooms", 
               "city",
               "maxprice",
               "minprice",
               "state")

baseURL = "https://www.apartments.com/"

pageattrs = {"data-listingid": True}
def formatbedroom(bedroom):
    """Returns bedroom type for URL query.
    :param bedroom: String or Integer."""
    if isinstance(bedroom, int):
        if bedroom <= 1:
            return 1
        elif bedroom >= 3:
            return 3
        return bedroom
    elif bedroom == "studios":
        return "studios"
    return None

def formatcost(minprice, maxprice):
    """Returns cost formatted for URL query.
    :param minprice: Minimum desired rent.
    :param maxprice: Maximum desired rent."""
    #I leave it to the user to give sensible min and max prices.
    if minprice is None:
        if maxprice is not None:
            if maxprice < 400:
                return "under-400"
            elif maxprice > 400:
                return f"under-{maxprice}"
            #If we're at THIS point, then someone gave a negative maxprice!
            return None
    elif maxprice is None:
        if minprice < 400:
            return "over-400"
        elif minprice > 400:
            return f"over-{minprice}"
        return None
    return f"{minprice}-to-{maxprice}"

def formatURL(**kwargs):
    """Formats a URL extension for apartments.com queries.
    :param bathrooms: Integer min number of bathrooms (1 - 3; 3 = 3+)
    :param bedrooms: Integer or String, number of bedrooms
    ("studio" or 1 - 4; 4 = 4+)
    :param city: String city name
    :param maxprice: Integer max price
    :param minprice: Integer min price
    :param state: String state abbreviation ("TX" good, "Texas" bad)
    """
    if "state" not in kwargs:
        raise NoStateException("Please provide a state in the USA.")
    
    specs = {key: kwargs.get(key, default=None) for key in descriptors}
    
    
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
        else:
            for function in ...:
                pass        


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
        
    # get the name of the property
    get_property_name(soup)
    # get the address of the property
    get_property_address(soup)
    # get the size of the property
    get_property_size(soup)
    # get the one time and monthly fees
    get_fees(soup)
    # get the images as a list
    get_images(soup)
    get_description(soup)
    # only look in this section (other sections are for example for printing)
    soup = soup.find('section', class_='specGroup js-specGroup')
    get_pet_policy(soup, fields)
    # get parking information
    get_parking_info(soup, fields)
    # get the amenities description
    get_field_based_on_class(soup, 'amenities', 'featuresIcon')
    # get the 'interior information'
    get_field_based_on_class(soup, 'indoor', 'interiorIcon', fields)
    # get the 'outdoor information'
    get_field_based_on_class(soup, 'outdoor', 'parksIcon', fields)
    # get the 'gym information'
    get_field_based_on_class(soup, 'gym', 'fitnessIcon', fields)
    # get the 'kitchen information'
    get_field_based_on_class(soup, 'kitchen', 'kitchenIcon', fields)
    # get the 'services information'
    get_field_based_on_class(soup, 'services', 'servicesIcon', fields)
    # get the 'living space information'
    get_field_based_on_class(soup, 'space', 'sofaIcon', fields)
    # get the lease length
    get_field_based_on_class(soup, 'lease', 'leaseIcon')
    # get the 'property information'
    get_features_and_info(soup)
    return fields

def get_field_based_on_class(soup, field, icon, fields):
    """Given a beautifulSoup parsed page, extract the specified field based on the icon"""    
    obj = soup.find('i', attrs={"class": "icon"})
    if obj is not None:
        data = obj.parent.findNext('ul').getText()
        data = prettify_text(data)

        fields[field] = data

def get_images(soup):
    """Get the images of the apartment."""
    # find ul with id fullCarouselCollection
    soup = soup.find('ul', {'id': 'fullCarouselCollection'})
    if soup is not None:
        #This is markdown.
        return " ".join(f"![{imgtag['alt']}]({imgtag['src']})"
                        for imgtag in soup.find_all("img"))


def get_description(soup):
    """Get the description for the apartment"""
    # find p with itemprop description
    obj = soup.find('p', {'itemprop': 'description'})
    if obj is not None:
        return cleantext(obj.getText())

def get_property_size(soup):
    """Get the property size of the first one bedroom."""
    #note: this might be wrong if there are multiple matches!!!
    fields['size'] = ''    
    obj = soup.find('tr', {'data-beds': '1'})
    if obj is not None:
        data = obj.find('td', class_='sqft').getText()
        data = prettify_text(data)
        fields['size'] = data


def get_features_and_info(soup):
    """Get features and property information."""
    
    obj = soup.find('i', class_='propertyIcon')

    if obj is not None:
        for obj in soup.find_all('i', class_='propertyIcon'):
            data = obj.parent.findNext('ul').getText()
            data = prettify_text(data)

            if obj.parent.findNext('h3').getText().strip() == 'Features':
                # format it nicely: remove trailing spaces
                fields['features'] = data
            if obj.parent.findNext('h3').getText() == 'Property Information':
                # format it nicely: remove trailing spaces
                fields['info'] = data


def get_parking_info(soup):
    """Given parking information."""   
    obj = soup.find('div', class_='parkingDetails')
    if obj is not None:
        data = obj.getText()
        data = prettify_text(data)

        # format it nicely: remove trailing spaces
        return data #strip?


def get_pet_policy(soup):
    """Get information on pet policy."""
    data = soup.find('div', {"class": "petPolicyDetails"})
    if data is None:
        data = ''
    else:
        data = data.getText()
        data = prettify_text(data)

    # format it nicely: remove the trailing whitespace
    fields['petPolicy'] = data


def get_fees(soup):
    """Get one time fees and monthly fees."""

    fields['monthFees'] = ''
    fields['onceFees'] = ''
    obj = soup.find('div', attrs={"class": "monthlyFees"})
    if obj is not None:
        for expense in obj.find_all('div', class_='fee'):
            description = expense.find(
                'div', class_='descriptionWrapper').getText()
            description = prettify_text(description)

            price = expense.find('div', class_='priceWrapper').getText()
            price = prettify_text(price)

            fields['monthFees'] += '* ' + description + ': ' + price + '\n'

    # get one time fees
    obj = soup.find('div', attrs={"class": "oneTimeFees"})
    if obj is not None:
        for expense in obj.find_all('div', class_='fee'):
            description = expense.find(
                'div', class_='descriptionWrapper').getText()
            description = prettify_text(description)

            price = expense.find('div', class_='priceWrapper').getText()
            price = prettify_text(price)

            fields['onceFees'] += '* ' + description + ': ' + price + '\n'

    # remove ending \n
    fields['monthFees'] = fields['monthFees'].strip()
    fields['onceFees'] = fields['onceFees'].strip()

propertynameattrs = {"itemprop": "name", "content": True}
def getpropertyname(articletag):
    """Return name of the property."""
    tag = articletag.find("meta", attrs=propertynameattrs)
    return cleantext(tag["content"])

from collections import namedtuple

addressattrs = {"itemprop": "streetAddress", "content": True}
cityattrs = {"itemprop": "addressLocality", "content": True}
regionattrs = {"itemprop": "addressRegion", "content": True}
zipcodeattrs = {"itemprop": "postalCode", "content": True}
def get_property_address(articletag):
    """Get full address of the property."""
    addresstag = articletag.find("meta", attrs=addressattrs)
    address = cleantext(addresstag["content"])

    citytag = articletag.find("meta", attrs=cityattrs)
    city = cleantext(citytag["content"])
    
    regiontag = articletag.find("meta", attrs=regionattrs)
    state = cleantext(regiontag["content"])

    zipcodetag = articletag.find("meta", attrs=zipcodeattrs)
    zipcode = cleantext(zipcodetag["content"])
    return (address, city, state, zipcode)


urlattrs = {"class": True, "href": True, "title": True}
def getpropertyurl(articletag):
    tag = articletag.find("a", attrs=urlattrs)
    return cleantext(tag["href"])


header = ('Option Name', 'Contact', 'Address', 'Size',
          'Rent', 'Monthly Fees', 'One Time Fees',
          'Pet Policy', 'Distance', 'Duration',
          'Parking', 'Gym', 'Kitchen', 'Amenities',
          'Features', 'Living Space', 'Lease Info', 'Services',
          'Property Info', 'Indoor Info', 'Outdoor Info',
          'Images', 'Description')


def getallinfo(page_url, map_info, writer, pscores):
    """Given the current page URL, extract the information from each apartment in the list"""

    soup = BS(page.text, 'html.parser')
    # append the current apartments to the list
    for item in soup.find_all('article', class_='placard'):
        url = ''
        rent = ''
        contact = ''

        if item.find('a', class_='placardTitle') is None: continue
        url = item.find('a', class_='placardTitle').get('href')

        # get the rent and parse it to unicode
        obj = item.find('span', attrs={"class": "altRentDisplay"})
        if obj is not None:
            rent = obj.getText().strip()

        # get the phone number and parse it to unicode
        phonenumbertag = item.find('div', attrs={"class": "phone"})
        if phonenumbertag is not None:
            phonenumber = cleantext(obj.getText())
        else:
            phonenumber = None            

        fields = parse_apartment_information(url, map_info)

        fields['name'] = '[' + fields['name'] + '](' + url + ')'
        fields['address'] = '[' + fields['address'] + '](' + fields['map'] + ')'

        # fill out the CSV file
        row = [fields['name'], contact,
               fields['address'], fields['size'],
               rent, fields['monthFees'], fields['onceFees'],
               fields['petPolicy'], fields['distance'], fields['duration'],
               fields['parking'], fields['gym'], fields['kitchen'],
               fields['amenities'], fields['features'], fields['space'],
               fields['lease'], fields['services'],
               fields['info'], fields['indoor'], fields['outdoor'],
               fields['img'], fields['description']]
        # add the score fields if necessary
        if pscores:
            for i in range(len(row), 0, -1):
                row.insert(i, '5')
            row.append('0')
        # write the row
        writer.writerow(row)

    # get the next page URL for pagination
    next_url = soup.find('a', attrs={"class": "next"})
    # if there's only one page this will actually be none
    if next_url is None:
        return None

    # get the actual next URL address
    next_url = next_url.get('href')

    # recurse until the last page
    if next_url is not None and next_url != 'javascript:void(0)':
        write_parsed_to_csv(next_url, map_info, writer, pscores)


def getlastpagenum(soup):
    """Gets last page from results."""
    #The footer of the results page lists pages containing at most 25
    #results each. So at the bottom of the landing page for a search that
    #would get 126 results, it would say <1 2 3 ... 6>. 25 results on each
    #of pages 1 (current), 2, 3, 4, and 5, but 1 result on page 6.

    result = soup.select("li div a")    
    return max(int(tag["data-page"]) for tag in result
               if not tag.has_attr("class"))
