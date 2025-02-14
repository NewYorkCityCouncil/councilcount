
<!-- README.md is generated from README.Rmd. Please edit that file -->

# Overview

The `councilcount` package allows easy access to population data for
over 100 demographic groups across various NYC geographic boundaries.
This data was pulled from the 5-Year American Community
Survey. For geographic boundaries that are not included in the ACS, like
council districts, estimates were generated. To view this data in an interactive format, 
please visit https://rnd.council.nyc.gov/councilcount/. 

## Installation

You can install the released version of `councilcount` from GitHub

``` r
remotes::install_github("newyorkcitycouncil/councilcount")
```

## Load Package

``` r
library(tidyverse)
# load last
library(councilcount)
```

## Vignette

For demos of the functions included in `councilcount`, please visit
`vignettes/councilverse.Rmd`.

## Quick Start

First load the `councilcount` package as above.

### Functions

#### R

`councilcount` includes 3 functions:

* `get_bbl_estimates()` – Generates a dataframe that provides population
estimates at the BBL level. There are also columns for latitude and longitude, which allow for
spatial joins if aggregation to other geography levels is desired.
* `get_geo_estimates()` – Creates a dataframe that provides population estimates for selected
demographic variables along chosen geographic boundaries (e.g. council
district, borough, etc.) for a chosen ACS 5-Year survey.
* `get_ACS_variables()` – Provides information on all of the available ACS demographic variables that can be
accessed via `get_geo_estimates()` for a specified survey year.

`get_bbl_estimates()` has 1 parameter:

* `year` – The desired year for BBL estimates. The years currently available are 2011, 2016, 2021, and 2022. 

`get_ACS_variables()` has 1 parameter:

* `acs_year` – The end-year of the desired 5-Year ACS. The surveys currently available are 2007-2011, 2012-2016, 2017-2021, and 2018-2022. 

`get_geo_estimates()` has 4 parameters:

* `acs_year` - The end-year of the desired 5-Year ACS. The surveys currently available are 2007-2011, 2012-2016, 2017-2021, and 2018-2022. 
* `geo` – The desired geographic region. Please select from the following
list:
   * Council Distrist: “councildist”
   * Community Distrist: “communitydist”
   * School District: “schooldist”
   * Police Precinct: “policeprct”
   * Neighborhood Tabulation Area: “nta”
   * Borough: “borough”
   * New York City: "city"
* `var_codes` – The desired demographic group(s), as represented
by the ACS variable code. To access the list of available demographic
variables and their codes, please run `get_ACS_variables()` for the desired survey year.
* `boundary_year` – If “councildist” is selected, the boundary year must
be specified as 2013 or 2023. The default is 2023.

Here is an example, in which codes for “Female” and “Adults with
Bachelor’s degree or higher” are used. The data is requested along 2023
Council District boundaries for the 2018-2022 ACS.

``` r
vars <- c('DP05_0003E', 'DP02_0068E')
get_geo_estimates(acs_year = "2022", geo = "councildist", var_codes = vars, boundary_year = "2023") 
```

#### Python

The equivalent functions are also available in Python. To access them,
use the following code:

Use pip to install the package in the terminal:
``` bash
pip install councilcount
```
Then import the package in Python:
``` python
import councilcount as cc
```

You can also download the package using the following code. You must have the `councilcount` package downloaded on your computer for this installation method:

``` python
import sys
my_path = 'INSERT PATH' # set absolute path to /councilcount/inst/python location (example: '/Users/jsmith/Desktop)
sys.path.insert(0, my_path + "/councilcount/inst/python/")
from retrieve_estimates import get_bbl_estimates, get_ACS_variables, get_geo_estimates
```

## Data Sources 

* [The Five Year American Community Survey (ACS)](https://www.census.gov/data/developers/data-sets/acs-5year.html)
  * 2006-2011
  * 2012-2016
  * 2017-2021
  * 2018-2022
* [Primary Land Use Tax Lot Output (PLUTO) datasets](https://www.nyc.gov/site/planning/data-maps/open-data/dwn-pluto-mappluto.page)
  * 2011
  * 2016
  * 2021
  * 2022  

## Methodology 

Estimates for over 100 ACS demographic variables were generated for the dashboard. Estimates are available at Council District, Community District, School District, Police Precinct, Neighborhood Tabulation Area, Borough, and New York City levels. CouncilCount utilizes the 5-Year ACS, meaning the data points presented on the dashboard represent 5-year averages for the listed demographic variables. Using the multiyear estimates increases the statistical reliability of the data, especially for small population subgroups and regions with low populations. 

These estimates were generated using the 2007-2011, 2012-2016, 2017-2021, and 2018-2022 ACS 5-Year Estimates Data Profiles, which provide demographic estimates by census tract. Estimates for some geographies, like neighborhood tabulation areas, which are built from census tracts, were generated by directly aggregating census-tract-level data. However, this method does not work for geographies that have no relation to census tracts, like council districts and police precincts. In order to generate estimates for such geographies, ACS demographic data was synthesized with building data from the 2011, 2016, 2021, and 2022 PLUTO datasets to approximate the distribution of subpopulations around the city for each time period. Estimates for all geographies (except for council districts, for which a boundary year must be specified) are available along boundary lines as they were drawn in 2020, regardless of the period chosen, in order to make comparisons possible across time. For more information on the method used to generate the demographic estimates presented on CouncilCount, please contact datainfo@council.nyc.gov.

