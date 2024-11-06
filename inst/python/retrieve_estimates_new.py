import pandas as pd
import numpy as np
from copy import deepcopy 
import geopandas as gpd
import os

path_str = os.path.dirname(__file__)
sub_str = "councilcount/" # initializing sub string
absolute_path = path_str[:path_str.index(sub_str) + len(sub_str)] # slicing off after length computation

# set possible geographies
geos = ['councildist13', 'councildist23', 'policeprct', 'schooldist', 'communitydist', 'nta', 'schooldist', 'borough', 'city']

# set ACS 5-Year years
acs_years = [2011, 2016, 2021]

# uploading data for all years
for year in acs_years:

  # paths for data dictionaries for ACS variable codes
  data_dict_relative_path = f'inst/extdata/data_dictionary_{year}.csv'
  data_dict_full_path = os.path.join(absolute_path, data_dict_relative_path)
  
  # path for BBL population estimates
  bbl_relative_path = f'inst/extdata/bbl-population-estimates_{year}.csv'
  bbl_full_path = os.path.join(absolute_path, bbl_relative_path)
  
  # paths for demographic dataframes
  nyc_relative_path = f'inst/extdata/nyc-wide_estimates_{year}.csv'
  nyc_full_path = os.path.join(absolute_path, nyc_relative_path)
  councildist13_relative_path = f'inst/extdata/council13-geographies_{year}.geojson'
  councildist13_full_path = os.path.join(absolute_path, councildist13_relative_path)
  councildist23_relative_path = f'inst/extdata/council23-geographies_{year}.geojson'
  councildist23_full_path = os.path.join(absolute_path, councildist23_relative_path)
  schooldist_relative_path = f'inst/extdata/schooldist-geographies_{year}.geojson'
  schooldist_full_path = os.path.join(absolute_path, schooldist_relative_path)
  communitydist_relative_path = f'inst/extdata/cd-geographies_{year}.geojson'
  communitydist_full_path = os.path.join(absolute_path, communitydist_relative_path)
  policeprct_relative_path = f'inst/extdata/policeprct-geographies_{year}.geojson'
  policeprct_full_path = os.path.join(absolute_path, policeprct_relative_path)
  nta_relative_path = f'inst/extdata/nta-geographies_{year}.geojson'
  nta_full_path = os.path.join(absolute_path, nta_relative_path)
  borough_relative_path = f'inst/extdata/borough-geographies_{year}.csv'
  borough_full_path = os.path.join(absolute_path, borough_relative_path)

  # uploading data dictionaries
  globals()[f'data_dictionary_{year}'] = pd.read_csv(data_dict_full_path)
  
  # uploading BBL population estimates
  globals()[f'population_estimates_{year}'] = pd.read_csv(bbl_full_path)
  
  # uploading demographic estimates
  globals()[f'nyc_wide_estimates_{year}'] = pd.read_csv(nyc_full_path).set_index('city')
  globals()[f'councildist13_geographies_{year}'] = gpd.read_file(councildist13_full_path).set_index('council13')
  globals()[f'councildist23_geographies_{year}'] = gpd.read_file(councildist23_full_path).set_index('council23')
  globals()[f'communitydist_geographies_{year}'] = gpd.read_file(communitydist_full_path).set_index('cd')
  globals()[f'schooldist_geographies_{year}'] = gpd.read_file(schooldist_full_path).set_index('schooldist')
  globals()[f'policeprct_geographies_{year}'] = gpd.read_file(policeprct_full_path).set_index('policeprct')
  globals()[f'nta_geographies_{year}'] = gpd.read_file(nta_full_path).set_index('nta')
  globals()[f'borough_geographies_{year}'] = gpd.read_file(borough_full_path).set_index('borough')

  # converting to GeoDataFrames 
  globals()[f'councildist13_geographies_{year}'] = globals()[f'councildist13_geographies_{year}'].to_crs(2263)
  globals()[f'councildist23_geographies_{year}'] = globals()[f'councildist23_geographies_{year}'].to_crs(2263)    globals()[f'policeprct_geographies_{year}'] = globals()[f'policeprct_geographies_{year}'].to_crs(2263)
  globals()[f'policeprct_geographies_{year}'] = globals()[f'policeprct_geographies_{year}'].to_crs(2263) 
  globals()[f'schooldist_geographies_{year}'] = globals()[f'schooldist_geographies_{year}'].to_crs(2263) 
  globals()[f'communitydist_geographies_{year}'] = globals()[f'communitydist_geographies_{year}'].to_crs(2263)     
  globals()[f'borough_geographies_{year}'] = globals()[f'borough_geographies_{year}'].to_crs(2263)
  globals()[f'nta_geographies_{year}'] = globals()[f'nta_geographies_{year}'].to_crs(2263)

####################################

def get_geo_estimates(geo, var_codes, acs_year, polygons = False, download = False):
    
    """
    Output:
      A dataframe containing demographic estimates for selected ACS 5-Year codes aggregated at a specified geography for a specified survey year
      
    Inputs:
      geo (str): the level of geographic aggregation
        select from 'councildist13', 'councildist23', 'policeprct', 'schooldist', 'communitydist', 'nta', 'schooldist', 'borough', 'city'
      var_codes (list or str): desired list of ACS variable codes OR the string 'all' to access all variables at once 
        use get_ACS_variables() to view options, variable information
      acs_year (str): the desired 5-Year ACS year
        ex: for the 2017-2021 5-Year ACS, enter '2021'
        select from '2011', '2016', '2021'
      polygons (bool): choose whether geographic polygon info will be included in a column called 'geometry'
        default = False
      download (bool): choose whether the dataframe will be downloaded upon running the function
        default = False
    
    """
    
    # error if geo not available
    if geo not in geos:
        raise ValueError(f'Estimates for the geography type {geo} are not available')
    
    # error if geo not available
    if acs_year not in acs_years:
        raise ValueError(f'Estimates for the {acs_year} ACS are not available')
    
    if geo != 'city': request_df = deepcopy(globals()[f'{geo}_geographies_{acs_year}'])
    else: request_df = deepcopy(globals()[f'nyc_wide_estimates_{acs_year}'])
    
    col_list = []
    
    # data dictionary containing all available var_codes
    data_dict = globals()[f'data_dictionary_{acs_year}']
    
    # when 'all' is the input, include all available variables
    if var_codes = 'all':
      
      var_codes = data_dict['var_codes'].to_list()
      
    else:
    
      # looking through all requested codes    
      for var_code in var_codes:
  
          # error if var_code not available
          if var_code not in data_dict['var_codes'].to_list():
              raise ValueError(f'Estimates for the variable code {var_code} are not available')
  
          elif var_code in data_dict['var_codes'].to_list():
            
            # adding # estimate, # MOE, % estimate, % MOE, and CV
            var_code_base = var_code[:9]
            col_list.append([var_code_base + 'E', 
                             var_code_base + 'M',
                             var_code_base + 'PE',
                             var_code_base + 'PM',
                             var_code_base + 'V'])
      
      # adding geometry
      if polygons and geo != 'city': # city doesn't have a geometry column
          
          col_list.append('geometry')
        
      # subsetting to all chosen columns
      request_df = request_df[col_list] 
        
    if download:
        
        if geo != 'city': request_df.to_file(f'demographic-estimates_by-{geo}_{acs_year}5YearACS.geojson')
        else: request_df.to_csv(f'nyc-wide_demographic-estimates_{acs_year}5YearACS.csv')
            
    return request_df

####################################

def get_bbl_estimates(year):
  
      """
    Output:
      A dataframe containing BBL-level population estimates for a specified year
      
    Inputs:
      year (str): the desired year for BBL-level estimates
      
    """
    
    return globals()[f'population_estimates_{year}']

####################################

def get_ACS_variables(acs_year):
    
    """
    Output:
      A dataframe containing the data dictionary with all available ACS codes for a specified survey year 
        Use this to determine possible inputs for get_geo_estimates()
      
    Inputs:
      acs_year (str): the desired 5-Year ACS year
        ex: for the 2017-2021 5-Year ACS, enter '2021'
    
    """
    
    return globals()[f'data_dictionary_{acs_year}']
