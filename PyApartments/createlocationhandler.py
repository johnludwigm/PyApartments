

import sqlite3
import csv

create_table_statement = ("CREATE TABLE Location ("    
                          "zipcode TEXT NOT NULL, "
                          "city TEXT NOT NULL, "
                          "state TEXT NOT NULL, "
                          "stateabbr TEXT NOT NULL, "
                          "county TEXT NOT NULL);")


create_index_statements = ("CREATE INDEX zipcodeidx ON Location(zipcode);",
                           "CREATE INDEX cityidx ON Location(city);",
                           "CREATE INDEX stateidx ON Location(city);",
                           "CREATE INDEX stateabbridx ON Location(stateabbr);",
                           "CREATE INDEX countyidx ON Location(county);")
                           


def formatcols(csvrow):
    """Pad the zip code to 5 digits and return a tuple."""
    return (csvrow[0].zfill(5), ) + tuple(csvrow[1: 5])


def createlocationdb(dbname, csvfile):
    conn = sqlite3.connect(dbname)
    cursor = conn.cursor()
    cursor.execute(create_table_statement)

    fieldnames = ("Zip Code", "Place Name", "State", "State Abbreviation",
                  "County", "Latitude", "Longitude")

    dbfields = ("Zip Code", "Place Name", "State", "State Abbreviation",
                "County")
    
    with open(csvfile, newline="", encoding="utf-8") as csvobj:
        readobj = csv.reader(csvobj)
        header = next(readobj)
        row = next(readobj)
        
        cursor.executemany("INSERT INTO Location VALUES (?,?,?,?,?);",
                           map(formatcols, readobj))
        

    for statement in create_index_statements:
        cursor.execute(statement)
    conn.commit()
    conn.close()


if __name__ == "__main__":
    createlocationdb("location.db", "us_postal_codes.csv")
        
