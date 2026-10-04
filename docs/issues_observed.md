
# Issues Observed – Lab 1

Based only on inspection of the raw file (`dirty_cafe_sales.csv`), the following problems were noticed:

1. All columns were loaded as text (string) even though Quantity, Price Per Unit and Total Spent should be numeric.
2. The value "ERROR" appears in the data (for example in Total Spent and Payment Method).
3. The value "UNKNOWN" appears in several columns (Item, Payment Method, Location, Transaction Date).
4. There are many missing values:

   - Location has 3,265 missing values
   - Payment Method has 2,579 missing values
   - Item has 333 missing values
   - Other columns also have missing values
5. Transaction Date contains the text "UNKNOWN" instead of a real date in some rows (159 times).
6. Some rows look inconsistent — for example a Quantity and Price Per Unit are present but Total Spent is recorded as "ERROR".
7. Location and Payment Method have a very high proportion of missing or placeholder values, which makes them less reliable.
