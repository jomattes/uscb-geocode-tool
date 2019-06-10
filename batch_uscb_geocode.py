'''
Description: Takes a large set of pre-formatted addresses and runs them through
the US Census Bureau's Geocoder API 10,000 at a time (max limit).

Author: Jon Mattes
'''

# load libraries
from tkinter import filedialog, Tk
import pandas as pd
import numpy
import io
import requests


# Helper Functions
#===============================================================================
def uscb_api_response(fname):
    # Loads a chosen .csv file into the US Census Bureau's Geocoder API and
    # retrieves the response data.
    #
    # Args:
    #   fname = A string value representing the file name of the chosen .csv
    #
    # Returns:
    #   The response data from the Geocoder API, hopefully including lat & lon
    #   values if the file was formatted correctly.
    api_url = 'https://geocoding.geo.census.gov/geocoder/locations/addressbatch?form'
    files = dict(addressFile = open(fname, 'rb'))
    data = dict(returntype = 'locations',
                benchmark = 'Public_AR_Current')

    # connect to api
    response = requests.post(api_url, files = files, data = data)

    # clean response data
    response_text = response.content
    try:
        response_data = pd.read_csv(io.StringIO(response_text.decode('latin-1')),
            names = numpy.arange(0,8), encoding = 'utf8', engine = 'python')
    except:
        try:
            response_data = pd.read_csv(io.StringIO(response_text.decode('latin-1')),
                names = numpy.arange(0,8), encoding = 'utf8', engine = 'c')
        except:
            try:
                response_data = pd.read_csv(io.StringIO(response_text.decode('utf-8')),
                    names = numpy.arange(0,8))
            except:
                try:
                    response_data = pd.read_csv(io.StringIO(response_text.decode('utf-8')),
                        names = numpy.arange(0,8), encoding = 'utf8', engine = 'c')
                except:
                    try:
                        response_data = pd.read_csv(io.StringIO(response_text.decode('utf-8')),
                            names = numpy.arange(0,8), encoding = 'utf8', engine = 'python')
                    except:
                        print('FAILURE TO PARSE. EXITING PROGRAM')
                        exit()

    return response_data
#===============================================================================

# Load in Address File
#===============================================================================
def load_addresses():
    # Loads a chosen address file into a pandas dataframe, while checking the
    # basic file structure.
    #
    # Args: None
    #
    # Returns:
    #   address_data = A pandas dataframe containing addresses to be geocoded.

    # start tkinter window, open file dialog, then close window
    root = Tk()
    filename = filedialog.askopenfilename(title = 'Choose Address File')
    root.destroy()

    # load file & check basic structure
    address_data = pd.read_table(filename, delimiter = '|')
    if len(address_data.columns) != 5:
        print('ERROR: Address file in incorrect format. Please refer to' +
        ' README file for format requirements.')
        exit()

    return address_data
#===============================================================================

# Main Loop Function
#===============================================================================
def uscb_geocode_loop(tbl, fin_tbl, loop_num, loop_cnt):
    # Splits a chosen table containing addresses to be geocoded into groups of
    # 10,000 (API limit) before pushing them to the US Census Bureau geocoder
    # API.  The resulting data is then cleaned and loaded into an overall
    # dataframe.
    #
    # Args:
    #   tbl = A pandas dataframe containing addresses to be geocoded
    #   fin_tbl = A blank pandas dataframe where geocoded addresses will be
    #             stored after every loop.
    #   loop_num = The number of loops required to geocode tbl.
    #   loop_cnt = The loop to start on.
    #
    # Returns:
    #   fin_tbl = A pandas dataframe containing geocoded addresses.
    while loop_cnt < loop_num:
        # determine start and end rows
        start_row = loop_cnt * 10000
        end_row = ((loop_cnt + 1) * 10000)
        if end_row > (loop_num * 10000):
            end_row = round(loop_num * 10000)

        # slice table
        use_tbl = tbl.iloc[start_row:end_row]

        # save as temporary csv
        use_tbl.to_csv('temp_geo.csv', index = False, header = False)

        # run API connection
        geo_temp = uscb_api_response('temp_geo.csv')

        # append api data to dataframe
        fin_tbl = fin_tbl.append(geo_temp)

        # loop finalizers
        loop_cnt += 1
        fin_tbl.to_csv('geocode_output.csv', index = False)
        print(f'Loops Completed: {loop_cnt}')
        print(f'Total Loops Needed: {loop_num}')
        print('Geocoded file available under "geocode_output.csv"')
        print('Exit program at any time and current output will be available')


    return fin_tbl
#===============================================================================


# Run
#===============================================================================
# get address data
address_data = load_addresses()

# start blank frame
geocoded_data = pd.DataFrame(columns = numpy.arange(0,8))

# initialize loop counters
N = len(address_data)
loop_num = N / 10000
loop_cnt = 0

# geocode
geocoded_data = uscb_geocode_loop(tbl = address_data,
                                  fin_tbl = geocoded_data,
                                  loop_num = loop_num,
                                  loop_cnt = loop_cnt)
#===============================================================================
