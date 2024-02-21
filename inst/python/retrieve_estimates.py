import pandas as pd
import numpy as np
from copy import deepcopy 
from geopandas import GeoDataFrame
from shapely import wkt
import os

path_str = os.path.dirname(__file__)
sub_str = "councilverse/" # initializing sub string
absolute_path = path_str[:path_str.index(sub_str) + len(sub_str)] # slicing off after length computation

bbl_relative_path = 'inst/extdata/bbl-population-estimates_2021.csv'
bbl_full_path = os.path.join(absolute_path, bbl_relative_path)

nyc_relative_path = 'inst/extdata/nyc-wide_estimates_2021.csv'
nyc_full_path = os.path.join(absolute_path, nyc_relative_path)
councildist13_relative_path = 'inst/extdata/councildist-geographies_b13_2021.csv'
councildist13_full_path = os.path.join(absolute_path, councildist13_relative_path)
councildist23_relative_path = 'inst/extdata/councildist-geographies_b23_2021.csv'
councildist23_full_path = os.path.join(absolute_path, councildist23_relative_path)
schooldist_relative_path = 'inst/extdata/schooldist-geographies_2021.csv'
schooldist_full_path = os.path.join(absolute_path, schooldist_relative_path)
communitydist_relative_path = 'inst/extdata/communitydist-geographies_2021.csv'
communitydist_full_path = os.path.join(absolute_path, communitydist_relative_path)
policeprct_relative_path = 'inst/extdata/policeprct-geographies_2021.csv'
policeprct_full_path = os.path.join(absolute_path, policeprct_relative_path)
nta_relative_path = 'inst/extdata/nta-geographies_2021.csv'
nta_full_path = os.path.join(absolute_path, nta_relative_path)
borough_relative_path = 'inst/extdata/borough-geographies_2021.csv'
borough_full_path = os.path.join(absolute_path, borough_relative_path)

# uploading BBL population estimates

population_estimates = pd.read_csv(bbl_full_path)

# NYC-level numbers for each demographic

nyc_wide_estimates = pd.read_csv(nyc_full_path)
# total_pop_NYC = 8769927 # council_geographies['Total population'].sum()
# total_house_NYC = 3250657 
# nyc_wide_estimates['Total population'] = total_pop_NYC

# uploading data for each geography type

councildist13_geographies = pd.read_csv(councildist13_full_path)
councildist23_geographies = pd.read_csv(councildist23_full_path)
communitydist_geographies = pd.read_csv(communitydist_full_path)
schooldist_geographies = pd.read_csv(schooldist_full_path)
policeprct_geographies = pd.read_csv(policeprct_full_path)
nta_geographies = pd.read_csv(nta_full_path)
borough_geographies = pd.read_csv(borough_full_path)

# fixing index/ columns

councildist13_geographies = councildist13_geographies.set_index('councildist13')
councildist23_geographies = councildist23_geographies.set_index('councildist23')
communitydist_geographies = communitydist_geographies.set_index('communitydist')
schooldist_geographies = schooldist_geographies.set_index('schooldist')
policeprct_geographies = policeprct_geographies.set_index('policeprct')
nta_geographies = nta_geographies.set_index('nta')
borough_geographies = borough_geographies.set_index('borough')

# converting to GeoDataFrames so choropleth map will read the geometry columns

councildist13_geographies['geometry'] = councildist13_geographies['geometry'].apply(wkt.loads)
council13_geographies = GeoDataFrame(councildist13_geographies, crs="EPSG:4326", geometry='geometry')
councildist23_geographies['geometry'] = councildist23_geographies['geometry'].apply(wkt.loads)
council23_geographies = GeoDataFrame(councildist23_geographies, crs="EPSG:4326", geometry='geometry')
communitydist_geographies['geometry'] = communitydist_geographies['geometry'].apply(wkt.loads)
communitydist_geographies = GeoDataFrame(communitydist_geographies, crs="EPSG:4326", geometry='geometry')
schooldist_geographies['geometry'] = schooldist_geographies['geometry'].apply(wkt.loads)
schooldist_geographies = GeoDataFrame(schooldist_geographies, crs="EPSG:4326", geometry='geometry')
policeprct_geographies['geometry'] = policeprct_geographies['geometry'].apply(wkt.loads)
policeprct_geographies = GeoDataFrame(policeprct_geographies, crs="EPSG:4326", geometry='geometry')
nta_geographies['geometry'] = nta_geographies['geometry'].apply(wkt.loads)
nta_geographies = GeoDataFrame(nta_geographies, crs="EPSG:4326", geometry='geometry')
borough_geographies['geometry'] = borough_geographies['geometry'].apply(wkt.loads)
borough_geographies = GeoDataFrame(borough_geographies, crs="EPSG:4326", geometry='geometry')

# all possible demographic dropdown items in Dash App have to be placed in a dictionary
# will be used to translate dropdown menu choices to codes used in the census api (50 variables at a time is the limit)

# variable names found at https://api.census.gov/data/2021/acs/acs5/profile/variables.html

# first 50 variables

# all available demographic estimates (variable codes are used by get_demo_estimates() to pull estimates from datasets)
# from https://api.census.gov/data/2021/acs/acs5/profile/variables.html

census_demo_variables = {'DP02_0088E':'Total population',
                           'DP02_0001E':'Total households',
                           'DP05_0071PE':'% Hispanic or Latino',
                           'DP05_0076PE':'% Not Hispanic or Latino',
                           'DP05_0039PE':'% American Indian and Alaska Native alone',
                           'DP05_0044PE':'% Asian alone',
                           'DP05_0038PE':'% Black or African American alone',
                           'DP05_0052PE':'% Native Hawaiian and other Pacific Islander alone',
                           'DP05_0037PE':'% White alone',
                           'DP05_0057PE':'% Some other race alone',
                           'DP05_0035PE':'% Two or more races',
                           'DP05_0079PE':'% American Indian and Alaska Native alone, not Hispanic or Latino',
                           'DP05_0080PE':'% Asian alone, not Hispanic or Latino',
                           'DP05_0078PE':'% Black or African American alone, not Hispanic or Latino',
                           'DP05_0081PE':'% Native Hawaiian and other Pacific Islander alone, not Hispanic or Latino',
                           'DP05_0077PE':'% White alone, not Hispanic or Latino',
                           'DP05_0082PE':'% Some other race alone, not Hispanic or Latino',
                           'DP05_0083PE':'% Two or more races, not Hispanic or Latino',
                           'DP05_0002PE':'% Male',
                           'DP05_0003PE':'% Female',
                           'DP05_0019PE':'% Under 18 years',
                           'DP05_0021PE':'% Over 18 years',
                           'DP05_0024PE':'% 65 years and over',
                           'DP02_0053E':'% Enrolled in school (3 years and over)',
                           'DP02_0054E':'% Enrolled in nursery school, preschool',
                           'DP02_0055E':'% Enrolled in Kindergarten',
                           'DP02_0056E':'% Enrolled in grades 1-8',
                           'DP02_0057E':'% Enrolled in grades 9-12',
                           'DP02_0058E':'% Enrolled in college, graduate school',
                           'DP02_0061E':'% Adults with no high school diploma',
                           'DP02_0062E':'% Adults with high school diploma (includes equivalency)',
                           'DP02_0068E':'% Adults with Bachelor\'s degree or higher',
                           'DP03_0002E':'% In the labor force (16 and older)',
                           'DP03_0007E':'% Not in the labor force (16 and older)',
                           'DP03_0004E':'% Employed (16 and older)',
                           'DP03_0005E':'% Unemployed (16 and older)',
                           'DP02_0090E':'% Born in the US',
                           'DP02_0093E':'% Born in Puerto Rico, U.S. Island areas, or abroad to American parents)',
                           'DP02_0094PE':'% Foreign born',
                           'DP02_0096E':'% Naturalized US citizen (foreign born)',
                           'DP02_0097E':'% Not a US citizen (foreign born)',
                           'DP02_0113E':'% Speak only English at home (5 years and older)',
                           'DP02_0115E':'% Speak English less than "very well" (5 years and older)',
                           'DP02_0116E':'% Speak Spanish at home (5 years and older)',
                           'DP02_0072E':'% With a disability (civilian, noninstitutionalized)',
                           'DP02_0074E':'% With a disability, under 18 (civilian, noninstitutionalized)',
                           'DP02_0076E':'% With a disability, over 18-65 (civilian, noninstitutionalized)',
                           'DP02_0078E':'% With a disability, over 65 (civilian, noninstitutionalized)',
                           'DP03_0096E':'% With health insurance (civilian, noninstitutionalized)',
                           'DP03_0097E':'% With private health insurance (civilian, noninstitutionalized)',
                           'DP03_0098E':'% With public coverage (civilian, noninstitutionalized)',
                           'DP03_0099E':'% With no health insurance coverage (civilian, noninstitutionalized)',
                           'DP03_0019E':'% Drive to work (workers 16 and older)',
                           'DP03_0020E':'% Carpool to work (workers 16 and older)',
                           'DP03_0021E':'% Take public transit to work (workers 16 and older)',
                           'DP03_0022E':'% Walk to work (workers 16 and older)',
                           'DP03_0024E':'% Work from home (workers 16 and older)',
                           'DP05_0005PE':'% Under 5 years',
                           'DP05_0006PE':'% 5 to 9 years',
                           'DP05_0007PE':'% 10 to 14 years',
                           'DP05_0008PE':'% 15 to 19 years',
                           'DP05_0009PE':'% 20 to 24 years',
                           'DP05_0010PE':'% 25 to 34 years',
                           'DP05_0011PE':'% 35 to 44 years',
                           'DP05_0012PE':'% 45 to 54 years',
                           'DP05_0013PE':'% 55 to 59 years',
                           'DP05_0014PE':'% 60 to 64 years',
                           'DP05_0015PE':'% 65 to 74 years',
                           'DP05_0016PE':'% 75 to 84 years',
                           'DP05_0017PE':'% 85 years and over'
                          }

####################################

def get_geo_estimates(geo, var_codes, polygons = False, download = False, demo_dict = census_demo_variables):
    
    if geo not in ['councildist13', 'councildist23', 'policeprct', 'schooldist', 'communitydist', 'nta', 'schooldist', 'borough', 'nyc']: # error if geo not available
        raise ValueError('Estimates for the geography type ' + geo + ' are not available')
    
    if geo != 'nyc': request_df = deepcopy(globals()[f'{geo}_geographies'])
    else: request_df = deepcopy(nyc_wide_estimates)
            
    col_name_list = []
        
    for var_code in var_codes:

        if var_code not in demo_dict.keys(): # error if var_code not available
            raise ValueError('Estimates for the variable code ' + var_code + ' are not available')

        if var_code in demo_dict.keys():

            col_name = demo_dict[var_code]

            col_name_list.append(col_name)

            if var_code not in ['DP02_0088E', 'DP02_0001E']: # these variables don't have MOE or CV
                col_name_list.append(col_name + ' MOE')
                col_name_list.append(col_name[2:] + ' CV')
    
    if polygons and geo != 'nyc':
        
        geometries = request_df['geometry']
        
        request_df = request_df[col_name_list]
        request_df['geometry'] = geometries
        
    else:
        
        request_df = request_df[col_name_list]
        
    if download:
        
        request_df.to_csv('demographic-estimates_by_' + geo + '.csv')
            
    return request_df

####################################

def get_bbl_estimates(pop_est_df = population_estimates):
    
    return pop_est_df

####################################

# outputs the available variables and their census api codes

def get_census_variables(demo_dict = census_demo_variables):
    
# demo_dict: the dict of available variable codes

    variable_df = pd.DataFrame(demo_dict.items(), columns=['var_code', 'var_name']) # df of each code/ variable name pairing  
    variable_df['var_name'] =  variable_df['var_name'].apply(lambda x: x[2:] if x not in ['Total population', 'Total households'] else x) # removing % from beginning of variable names
        
    return variable_df
