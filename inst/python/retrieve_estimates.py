import os
import pandas as pd
import geopandas as gpd
from warnings import warn

path_str = os.path.dirname(__file__)
sub_str = "councilcount/" # initializing sub string
absolute_path = path_str[:path_str.index(sub_str) + len(sub_str)] # slicing off after length computation


def get_geo_estimates(acs_year=None, geo=None, var_codes="all", boundary_year=None):
    """
    Retrieve demographic estimates by specified geography and ACS year.

    Parameters:
    acs_year (int): Desired 5-Year ACS year (e.g., "2021" for the 2017-2021 5-Year ACS).
    geo (str): Geographic level of aggregation desired. Options include "borough", "communitydist", "councildist", 
               "nta", "policeprct", "schooldist", or "city".
    var_codes (list or str): List of chosen variable codes selected from `get_ACS_variables()` 'estimate_var_codes'
    columns. Default is "all", which provides estimates for all available variable codes.
    boundary_year (int): Year for the geographic boundary (relevant for "councildist"). Options: "2013", "2023".

    Returns:
    pandas.DataFrame or geopandas.GeoDataFrame: A dataframe with estimates for the specified geography and ACS year,
    which can be found here: https://api.census.gov/data/{INSERT YEAR}/acs/acs5/profile/variables.html. 

    Notes:
    All variables are taken from the 5-Year ACS Data Profiles data dictionary. Codes ending with 'E' and 
    'M' represent numerical estimates and margins of error, respectively, while codes ending with 'PE' and 'PM'
    represent percent estimates and margins of error, respectively. Codes ending with 'V' represent coefficients of variation.
    """
    
    if acs_year: acs_year = int(acs_year) # so don't get error if accidentally input wrong dtype

    # find the directory with the data files
    extdata_path = f'{absolute_path}inst/extdata'

    # locate available CSV files
    file_names = os.listdir(extdata_path)
    geo_file_names = [f for f in file_names if "geographies" in f or "nyc-wide" in f]
    geo_names = list(set([f.split('-')[0] for f in geo_file_names]))
    geo_names.remove('nyc')
    geo_names.append('city')

    # record available years
    available_years = sorted(set(int(f.split('_')[-1][:4]) for f in file_names if f.split('_')[-1][:4].isdigit()))

    # boundary year information
    boundary_year_num = str(boundary_year)[-2:] if boundary_year else None

    def read_geos(geo, boundary_year_ext=None):
        """
        Internal function to read and wrangle geo files.
        """
        
        # preparing to access files with boundary year in name
        add_boundary_year = f"_b{boundary_year_ext}" if boundary_year_ext else ""
        
        # building paths
        if geo == "city":
            file_path = f'{extdata_path}/nyc-wide_estimates_{acs_year}.csv'
            geo_df = pd.read_csv(file_path)
        else:
            file_path = f'{extdata_path}/{geo}-geographies{add_boundary_year}_{acs_year}.geojson'
            geo_df = gpd.read_file(file_path).set_crs(epsg=2263)

        # if list of variable codes requested, subset
        if var_codes == "all": 
            return geo_df
        
        # if list of variable codes requested, subset
        else: 
            
            # list of columns for chosen variable(s) if "all" NOT selected
            master_col_list = [geo] 
            
            # creating list of desired variables names (for sub-setting final table)
            for var_code in var_codes:  
                
                # check if the variable code is available in the data
                if var_code not in geo_df.columns:
                    raise ValueError(f"Estimates for the variable code {var_code} are not available. Check for any typos.\n"
                                     "View available variable codes using get_ACS_variables(), or input 'all' to view all columns.")
                else:
                    var_code_base = var_code[:9]
                    var_col_list = [
                        f"{var_code_base}E",  # numeric estimate
                        f"{var_code_base}M",  # numeric MOE
                        f"{var_code_base}PE", # percentage estimate
                        f"{var_code_base}PM", # percentage MOE
                        f"{var_code_base}V"  # coefficient of Variation
                    ]
                    
                    # updating master column list
                    master_col_list.extend(var_col_list)
                    
            return geo_df[master_col_list + ['geometry']] # adding all desired columns + geometry column 

    # check input cases
    if acs_year is None:
        raise ValueError("`acs_year` parameter is required. Available options are:\n" +
                         ", ".join(map(str, available_years)))
    elif geo is None:
        raise ValueError("`geo` parameter is required. Available options are:\n" +
                         ", ".join(geo_names))
    elif geo == "councildist" and str(boundary_year) not in ["2013", "2023"]:
        warn("`boundary_year` must be set to 2013 or 2023 when `geo` is 'councildist'. Defaulting to 2023.")
        boundary_year_num = "23"
        return read_geos(geo, boundary_year_num)
    elif acs_year not in available_years:
        raise ValueError(f"The ACS year {acs_year} could not be found. Available options are:\n" +
                         ", ".join(map(str, available_years)))
    elif geo not in geo_names:
        raise ValueError(f"The geography '{geo}' could not be found. Available options are:\n" +
                         ", ".join(geo_names))
    elif geo != "councildist" and boundary_year is not None:
        warn("`boundary_year` is only relevant for `geo = councildist`. Ignoring `boundary_year` input.")
        return read_geos(geo)
    else:
        return read_geos(geo, boundary_year_num)

############################

def get_bbl_estimates(year=None):
    """
    Produces a dataframe containing BBL-level population estimates for a specified year.

    Parameters:
    year (str): The desired year for BBL-level estimates. If None, the most recent year available will be used.

    Returns:
    pandas.DataFrame: A table with population estimates by BBL, including multiple geography columns for aggregation. 
                      Avoid using estimates for individual BBLs; the more aggregation, the less error.
    """
    if year: year = str(year) # so don't get error if accidentally input wrong dtype
        
    # find the directory with the data files
    extdata_path = f'{absolute_path}inst/extdata'
    
    # find all available years
    csv_names = [f for f in os.listdir(extdata_path) if f.endswith(".csv")]
    bbl_csv_names = [name for name in csv_names if "bbl-population-estimates_" in name]
    bbl_years = [name[25:29] for name in bbl_csv_names]
    
    # if year is not chosen, set default to latest year
    if year is None:
        year = max(bbl_years)
    
    # construct the name of the dataset based on the year
    bbl_name = f"bbl-population-estimates_{year}.csv"
    
    # error message if unavailable survey year selected
    if year not in bbl_years:
        available_years = "\n".join(bbl_years)
        raise ValueError(
            f"This year is not available.\n"
            f"Please choose from the following:\n{available_years}"
        )
    
    print(f"Printing BBL-level population estimates for {year}")
    
    # retrieve the dataset
    file_path = f'{extdata_path}/{bbl_name}'
    df = pd.read_csv(file_path)
    
    return df

############################

def get_ACS_variables(acs_year=None):
    """
    Retrieve the available ACS demographic variables and their codes for a specified survey year.

    Parameters:
    acs_year (str): Desired 5-Year ACS year (e.g., for the 2017-2021 5-Year ACS, enter "2021").
                    If None, the most recent year available will be used.

    Returns:
    pd.DataFrame: Table of available variables with columns for variable code, variable name, 
                  denominator code, and denominator name (the "denominator variable" is the 
                  denominator population in percent estimate calculations). Use variable codes
                  as the input for `var_codes` in get_geo_estimates().

    Raises:
    ValueError: If the requested year is not available.
    """
    
    if acs_year: acs_year = str(acs_year) # so don't get error if accidentally input wrong dtype
    
    # find the directory with the data files
    extdata_path = f'{absolute_path}inst/extdata'

    # find all the available years
    csv_names = [f for f in os.listdir(extdata_path) if f.endswith(".csv")]
    dictionary_csv_names = [name for name in csv_names if "data_dictionary" in name]
    dictionary_years = [name[16:20] for name in dictionary_csv_names]

    # if year is not chosen, set default to the latest year
    if acs_year is None:
        acs_year = max(dictionary_years)

    # construct the name of the dataset based on the year
    dict_name = f"data_dictionary_{acs_year}.csv"

    # error message if the requested year is unavailable
    if acs_year not in dictionary_years:
        available_years = "\n".join(dictionary_years)
        raise ValueError(
            f"This year is not available.\n"
            f"Please choose from the following:\n{available_years}"
        )

    print(f"Printing data dictionary for the {acs_year} 5-Year ACS")

    # Retrieve the data dictionary
    file_path = f'{extdata_path}/{dict_name}'
    df = pd.read_csv(file_path)

    return df
