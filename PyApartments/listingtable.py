
#################################
#Apply to individual listings in#
# the table on a property page. #
#################################

import re

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
def getrent(tablerowsoup):
    """Returns list of rent prices.
    If rent for a listing is given as a range (minprice - maxprice),
    returns [(int) minprice, (int) maxprice].
    
    Otherwise, returns [(int) rent].
    """
    renttag = tablerowsoup.find("td", attrs=rentattrs)
    if renttag is None:
        return [None]
    return resolvenumbers(renttag.text.strip("$ "))
    

sqftattrs = {"class": "sqft"}
def getsqft(tablerowsoup)
    """Returns int number of square feet for listing."""
    sqfttag = tablerowsoup.find("td", attrs=sqftattrs)
    content = sqfttag.text
    if not content:
        return [None]
    return resolvenumbers(content.strip("Sq Ft"))


availableattrs = {"class": "available"}
def getavailability(tablerowsoup):
    """Returns string availability status of listing."""
    availabletag =  tablerowsoup.find("td", attrs=availableattrs)
    return availabletag.text.strip()


depositattrs = {"class": ["deposit", ""]}
def getdeposit(tablerowsoup):
    """Returns integer deposit."""
    deposittag = tablerowsoup.find("td", attrs=depositattrs)
    return resolvenumbers(deposittag.text.strip(" $"))[0]



unitattrs = {"class": "unit"}
def getunit(tablerowsoup):
    """Returns string identifying the listed unit."""
    unittag = tablerowsoup.find("td", attrs=unitattrs)
    returnstr = unittag.text.strip()
    return returnstr if returnstr != "" else None


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
     sqft, int,
     unit: str}     
    """
    returndict = {"bathrooms": int(tablerowsoup["data-baths"]),
                  "bedrooms": int(tablerowsoup["data-beds"]),
                  "model": tablerowsoup["data-model"],
                  "rentalkey": tablerowsoup["data-rentalkey"]}
    #maxrent = tablerowsoup["data-maxrent"]
    rent = getrent(tablerowsoup)
    if len(rent) == 2:
        returndict["minprice"], returndict["maxprice"] = rent
    else:
        returndict["rent"] = rent[0]

    returndict["sqft"] = getsqft(tablerowsoup)[0]
    returndict["availability"] = getavailability(tablerowsoup)
    returndict["unit"] = getunit(tablerowsoup)
    returndict["deposit"] = getdeposit(tablerowsoup)
    return returndict
