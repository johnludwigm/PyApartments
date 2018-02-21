
#################################
#Apply to individual listings in#
# the table on a property page  #
#################################

import decimal

def getprice(cashstring):
    """Returns Decomial amount of currency from cashstring."""
    return decimal.Decimal(cashstring.strip("$").replace(",", ""))

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

    deposit 
    
