#' Function to retrieve demographic estimates by specified geography and ACS year
#'
#' @import tidyverse
#' @import dplyr
#' @param acs_year (string). The desired 5-Year ACS year (ex: for the 2017-2021 5-Year ACS, enter "2021").
#' @param geo (string). Geographic level of aggregation desired. Options: "borough", "communitydist", "councildist", "nta", "policeprct", "schooldist", "city".
#' @param var_codes (list). List of chosen variable codes, selected from get_ACS_variables(). The default input is "all", which provides estimates for all available variable codes.
#' @param boundary_year (string). Year for the geographic boundary (i.e. `geo`). Currently only relevant for council districts, which have the options "2013" and "2023".
#' @return Table with estimates for the specified geography, ACS year. All variables are taken from the 5-Year ACS Data Profiles data dictionary, which can be found here: https://api.census.gov/data/{INSERT YEAR}/acs/acs5/profile/variables.html.
#' @export

get_geo_estimates <- function(acs_year = NULL, geo = NULL, var_codes = "all", boundary_year = NULL) {

  # locate available csv files
  file_names <- dir(system.file("extdata", package = "councilcount"))
  geo_file_names <- file_names[grepl("geographies|nyc-wide", file_names)]
  geo_names <- stringr::str_extract(geo_file_names, "[^-]+") %>% unique()
  geo_names[['nyc']] <- 'city'

  # recording available years
  available_years <- sort(as.numeric(unique(stringr::str_extract(file_names, "\\d{4}"))))

  # use boundary year information to collect the correct csv later
  boundary_year_num <- stringr::str_sub(as.character(boundary_year), -2)

  # function to read and wrangles geo files
  read_geos <- function(geo = NULL, boundary_year_ext = NULL) {

    if (!(is.null(boundary_year_ext))) { # if boundary_year not null (i.e. councildist is chosen), prepare to add boundary year to geo name
      add_boundary_year <- paste0('_b', boundary_year_ext) # putting in format that matches file names
    } else { # otherwise, leave as blank (no boundary year added)
      add_boundary_year <- ''
    }

    # creating output sf

    if (geo == 'city') {
      geo_df <- read_csv(system.file("extdata", glue::glue("nyc-wide_estimates_{acs_year}.csv"), package = "councilcount"))
    } else { geo_df <- sf::st_read(fs::path_package("extdata",glue::glue("{geo}-geographies{add_boundary_year}_{acs_year}.geojson"), package = "councilcount")) %>%
      sf::st_as_sf(wkt = "geometry", crs = 2263) # setting CRS to 2263 for NYC
    }

    master_col_list <- c(geo) # list of columns for chosen variable(s) if "all" NOT selected

    if ("all" %in% var_codes) { # if all variable codes chosen, output all columns
      return(geo_df)
    } else { # if list of variable codes requested, subset

      # creating list of desired variables names (for sub-setting final table)
      for (var_code in var_codes) {

        # check if the variable code is available in the data
        if (!(var_code %in% colnames(geo_df))) {
          stop(paste("Estimates for the variable code", var_code, "are not available", "\n",
                     "You may have made a typo, so please double check your work.", "\n",
                     "You can use the get_census_variables() function to view your variable options, or input 'all' to view all columns.\n"))
        } else {

          # add num estimate, num MOE, % estimate, % MOE, and CV for the variable code
          var_code_base <- substr(var_code, 1, 9)
          var_col_list <- c(paste0(var_code_base, 'E'),
                            paste0(var_code_base, 'M'),
                            paste0(var_code_base, 'PE'),
                            paste0(var_code_base, 'PM'),
                            paste0(var_code_base, 'V'))

          master_col_list <- append(master_col_list, var_col_list) # updating master column list

          }
        }
      return(geo_df[,master_col_list]) # subsetted
      }
    }

  # different input cases. can check in tests/testthat/test-get_geo_estimates_function.R

  if (is.null(acs_year)) {
    message("get_geo_estimates() requires an `acs_year` parameter.", "\n",
            "Please choose from the following:\n",
            paste0('"',available_years, '"', collapse = "\n"))
  } else if (is.null(geo)) {
    message("get_geo_estimates() requires a `geo` parameter.", "\n",
            "Please choose from the following:\n",
            paste0('"',geo_names, '"', collapse = "\n"))
  } else if (is.null(boundary_year) && geo == "councildist"){
    message("`boundary_year` input has been ommitted.", "\n",
            "`boundary_year` must be set to 2013 or 2023 when 'councildist' is selected for `geo`.", "\n",
            "Overriding `boundary_year` input to 2023.")
    read_geos(geo, "23")
  } else if (!(acs_year %in% available_years)) {
    message(paste0("The ACS year ", '"',acs_year,'"', " could not be found"), "\n",
            "Please choose from the following:\n",
            paste0('"',available_years, '"', collapse = "\n"))
  } else if (!(geo %in% geo_names)) {
    message(paste0("The geography ", '"',geo,'"', " could not be found"), "\n",
            "Please choose from the following:\n",
            paste0('"',geo_names, '"', collapse = "\n"))
  } else if ((boundary_year != "2013" & boundary_year != "2023") && geo == "councildist") {
    message(paste0('"',boundary_year, '"', " is not a valid input for `boundary_year`."), "\n",
            "`boundary_year` must be set to 2013 or 2023 when 'councildist' is selected for `geo`.", "\n",
            "Overriding `boundary_year` input to 2023.")
    read_geos(geo, "23")
  } else if (!is.null(boundary_year) && geo != "councildist"){
    message("`boundary_year` is only relevant for `geo = councildist`.", "\n",
            "Overriding `boundary_year` input to NULL.")
    read_geos(geo)
  } else if (is.null(boundary_year) && geo != "councildist"){ # correct entry for non-council geography
    read_geos(geo)
  } else if (geo == "councildist"){ # correct entry for council geography
    read_geos(geo, boundary_year_num)
  }
}

