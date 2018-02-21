# PyApartments
Apartments.com API for Python. Originating as scraper.




* Unit tests to come! I typically use the builtin `unittest` library, but I have seen lots of praise for `pytest`. The drawback for `pytest` is that it's not a builtin and therefore won't receive the continued support that `unittest` does.

* Will store ZIP codes, city names, state names, and county names in a SQLite database to improve search functionality.

* Eventually store either photo URLs or the photos themselves. The second option is less likely.


* Also might want to just collect a list of properties and periodically check their listings.