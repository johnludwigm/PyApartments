
#################################
#Apply to individual listings in#
# the table on a property page  #
#################################

import re

numberpattern = re.compile("[\d,]+")

rentattrs = {"class": "rent"}
def getrent(tablerowsoup):
    """Returns list of rent prices.
    If rent for a listing is given as a range (minprice - maxprice),
    returns [(int) minprice, (int) maxprice].
    
    Otherwise, returns [(int) rent].
    """
    renttag = tablerowsoup.find("td", attrs=rentattrs)
    if renttag is None:
        return [None]
    prices = [int(price.replace(",", "")) for
              price in numberpattern.findall(renttag.text.strip())]
    return prices


sqftattrs = {"class": "sqft"}
def getsqft(tablerowsoup):
    """Returns int number of square feet for listing."""
    sqfttag = tablerowsoup.find("td", attrs=sqftattrs)
    content = sqfttag.text
    if not content:
        return None
    return int(content.strip("Sq Ft").replace(",", ""))


availableattrs = {"class": "available"}
def getavailability(tablerowsoup):
    """Returns string availability status of listing."""
    availabletag =  tablerowsoup.find("td", attrs=availableattrs)
    return availabletag.text.strip()


def getdata(tablerowsoup):
    """Returns dictionary:
    :param tablerowsoup: tablerow <tr> tag in listing table
    on the property page

    Returns dictionary:
    {availability: str,
     bathrooms: int,
     bedrooms: int,
     deposit: int,
     maxprice: int,
     minprice: int,
     model: str,
     rentalkey: str,
     rent: int,
     sqft, int}     
    """
    returndict = {"bathrooms": int(tablerowsoup["data-baths"]),
                  "bedrooms": int(tablerowsoup["data-beds"]),
                  "model": tablerowsoup["data-model"],
                  "rentalkey": tablerowsoup["data-rentalkey"]}
    maxrent = tablerowsoup["data-maxrent"]

    rent = getrent(tablerowsoup)
    if len(rent) == 2:
        returndict["minprice"], returndict["maxprice"] = rent
    else:
        returndict["rent"] = rent[0]

    returndict["sqft"] = getsqft(tablerowsoup)
    returndict["availability"] = getavailability(tablerowsoup)
    
    
