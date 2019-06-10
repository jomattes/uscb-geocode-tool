# OVERVIEW

The Geocode App is a set of tools to geocode a file of addresses using the US
Census Bureau's Geocoder API.

### Geocoder Tool:
https://geocoding.geo.census.gov/geocoder/
### Geocoder API Documentation:
https://geocoding.geo.census.gov/geocoder/Geocoding_Services_API.pdf

## Geocode Accuracy Tool (geocode_accuracy_tool.py)

The Geocode Accuracy Tool allows a user to sample the address data in a text
file to determine the estimated geocoding accuracy without having to geocode the
entire dataset.

Using the tool:
1. Load project virtual environment (see above)
2. Create an address file according to the following specifications:
  -must have these columns, in order: AddressID, address, city, st, zip
  -must be in pipe-delimited format text file
3. Run the program, and point the file dialog box to the address file when
   appropriate

References:
Scheaffer, Richard L., et al. Elementary Survey Sampling.
     Vol. 7, Duxbury Resource Center, 2012. pg. 93

## Batch US Census Bureau Geocoder (batch_uscb_geocode.py)

The Batch Geocoder allows a user to upload a large file containing addresses to
the US Census Bureau's Geocoder API for the purposes of geocoding.  The program
loads in a chosen file, splits it into increments of 10,000, and feeds each
increment to the API in sequence.  The output will be saved under
'geocode_output.csv'.

Using the tool:
1. Load project virtual environment (see above)
2. Create an address file according to the following specifications:
  -must have these columns, in order: AddressID, address, city, st, zip
  -must be in pipe-delimited format text file
3. Run the program, and point the file dialog box to the address file when
   appropriate
