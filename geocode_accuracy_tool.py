'''
Description: Checks the accuracy of the US Census Bureau's Geocoder API on a
chosen file.

Author: Jon Mattes
'''

# load libraries
import pandas as pd
import requests
from tkinter import filedialog, Tk
import math
import io
import numpy

# Helper Functions
#===============================================================================
def prop_sample_size(x, p = 0.5, B = 0.02):
    # Calculates the sample size required to estimate a proportion with a bound
    # on the error of estimation based on the length of a given object.
    #
    # Args:
    #   x  = An object that represents the population from which to sample
    #   p = The estimated population proportion.  Defaults to 0.5 to represent
    #       a conservative sample size.
    #   B = A bound on the error of estimation.  Defaults to 0.02, or 2
    #       percentage points.
    #
    # Returns:
    #   An integer that represents the minimum sample size needed to estimate
    #   the population proportion given the above arguments.
    N = len(x)  # population size
    q = 1 - p
    D = B**2 / 4
    n = (N*p*q) / ((N-1)*D + p*q)
    return math.ceil(n)
#===============================================================================

# Create Sample File
#===============================================================================
def sample_address(savename):
    # Loads addresses and creates a sample from them in order to estimate the
    # accuracy of the USCB Geocoder API.  The chosen file (from the file dialog)
    # must match the exact specifications in the README file.
    #
    # Args:
    #   savename = A string value representing the name which the sample file
    #              should be saved under.
    #
    # Returns:
    #   A saved .csv file with a sample of the address data chosen.

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

    # calculate number of samples needed for good estimate
    sample_size = prop_sample_size(address_data)

    # create sample file and save as sample_geo.csv
    address_sample = address_data.sample(n = sample_size, random_state = 133)
    address_sample.to_csv(savename, index = False, header = False)
#===============================================================================

# Get Geocode Accuracy
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
    response_data = pd.read_csv(io.StringIO(response_text.decode('latin-1')), names = numpy.arange(0,8), encoding = 'utf8', engine = 'python')
    return response_data

def get_sample_acc(tbl):
    # Loads a chosen dataframe of geocoded values from the US Census Bureau's
    # Geocoder API and calculates the amount geocoded correctly.
    #
    # Args:
    #   tbl = A dataframe with geocoded values
    #
    # Returns:
    #   Print outs of matching percent and individual counts of matching types.
    match_types = tbl.iloc[:,3]
    sample_size = len(tbl)
    exact_match = len(match_types[match_types == 'Exact'])
    non_exact_match = len(match_types[match_types == 'Non_Exact'])
    no_match = len(match_types[match_types.isnull()])
    overall_per = round(((exact_match + non_exact_match)/sample_size) * 100, 2)

    # print out matching percents and counts
    print(f'Overall Match Percent = {overall_per}')
    print(f'Exact Matches = {exact_match}')
    print(f'Non Exact Matches = {non_exact_match}')
    print(f'No Matches = {no_match}')
#===============================================================================

# Run Functions
#===============================================================================
sample_address('sample_geo.csv')
response_data = uscb_api_response('sample_geo.csv')

get_sample_acc(response_data)
#===============================================================================
