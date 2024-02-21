#' Function to retrieve acs estimates from csvs at different geographies
#'
#' @param geo (string). Name of the geography with associated csv in "extdata". If NULL, returns a list of possible geography csvs. Options: "borough", "communitydist", "councildist", "nta", "policeprct", "schooldist".
#' @param var_codes (list). List of chosen variable codes, selected from get_census_variables. If wish to select all variable codes, input "all" (this is also the default value).
#' @param boundary_year (string). Year for the geographic boundary (i.e. geo). Currently only relevant for council districts, which have the options "2013" and "2023".
#' @import dplyr
#' @return sf for the specified geography, or message with list of geographies if none is specified
#' @export

get_geo_estimates <- function(geo = NULL, var_codes = "all", boundary_year = NULL) {

  # locate available csv files
  csv_names <- dir(system.file("extdata", package = "councilcount"))
  geo_csv_names <- csv_names[grepl("geographies", csv_names)]
  geo_names <- stringr::str_extract(geo_csv_names, "[^-]+") %>% unique()

  # df with var_codes that access desired variables
  demo_variables <- councilcount::census_demo_variables

  # use boundary year information to collect the correct csv later
  boundary_year_num <- stringr::str_sub(boundary_year, -2)

  # function to read and wrangles geo csv's
  # note: only year used so far is 2021 so all files end in _2021

  read_geos <- function(geo = NULL, boundary_year_ext = NULL) {

    if (!(is.null(boundary_year_ext))) { # if boundary_year not null (i.e. council is chosen), adding boundary year to geo name
      add_year <- stringr::str_sub(boundary_year_ext, 3)
    } else { # otherwise, leave as null (no boundary year added)
      add_year <- boundary_year_ext
    }

    # creating output df
    geo_df <- readr::read_csv(fs::path_package("extdata",glue::glue("{geo}-geographies{boundary_year_ext}_2021.csv"), package = "councilcount")) %>%
      janitor::clean_names() %>%
      sf::st_as_sf(wkt = "geometry", crs = 4326) %>%
      sf::st_transform("+proj=longlat +datum=WGS84")

    if ("all" %in% var_codes) { # if all variable codes chosen, output all columns
      return(geo_df)
    } else { # if list of variable codes requested, subset

      # using var_codes list to access desired variable names
      demo_variables <- demo_variables %>%
        mutate(cleaned_name = janitor::make_clean_names(var_name)) %>%
        filter(var_code %in% var_codes)

      # creating list of desired variables names (for sub-setting final df)
      col_names <- c(paste(geo, add_year, sep=''), 'geometry')
      for(i in 1:nrow(demo_variables)) {
        row <- demo_variables[i,]

        # if Total population/ households selected, only include estimate (doesn't have MOE/ CV)
        if (row$var_code %in% c('DP02_0088E','DP02_0001E')) {

          col_names <- append(col_names, row$cleaned_name)

        } else { # otherwise include estimates and MOE/ CV

          col_names <- append(col_names, row$cleaned_name) # adding percent version
          col_names <- append(col_names, stringr::str_sub(row$cleaned_name, 9)) # adding number   version
          col_names <- append(col_names, paste(row$cleaned_name, 'moe', sep = '_')) # adding % MOE
          col_names <- append(col_names, paste(stringr::str_sub(row$cleaned_name, 9), 'moe', sep = '_')) # adding number MOE
          col_names <- append(col_names, paste(stringr::str_sub(row$cleaned_name, 9), 'cv', sep = '_')) # adding CV
        }
      }
      return(geo_df[,col_names])
    }
  }

  # creating list of variable code typos if any are present
  typos <- c()
  if (!(is.null(var_codes))) {
    if (!("all" %in% var_codes)) { # if specific variable codes provided, check for typos
      typos <- var_codes[!(var_codes %in% demo_variables$var_code)]
    }
  }

  # different input cases. can check in tests/testthat/test-get_geo_estimates_function.R

  if (is.null(var_codes)) {
    message("get_geo_estimates() requires a 'var_codes' parameter.", "\n", "Please use the get_census_variables() function to view your options, or input 'all' to view all columns.\n")
  } else if (is.null(geo)) {
    message("get_geo_estimates() requires a 'geo' parameter.", "\n",
            "Please choose from the following:\n",
            paste0('"',geo_names, '"', collapse = "\n"))
  } else if ("2013" %in% var_codes | "2023" %in% var_codes){
    message("boundary_year input used for var_codes parameter. Please provide parameter names to avoid this issue.")
  } else if (length(typos) > 0){
    message("The following variable codes could not be found:\n\n", paste0('"',typos, '"', collapse = "\n"), "\n\nPlease use the get_census_variables() function to view your options, or input 'all' to view all columns.")
  } else if (!(geo %in% geo_names)) {
    message("This geography could not be found", "\n",
            "Please choose from the following:\n",
            paste0('"',geo_names, '"', collapse = "\n"))
  } else if (is.null(boundary_year) & geo == "councildist"){
    message("Setting `boundary_year` as 2013. `boundary_year` can be '2013' or '2023'.")
    read_geos(geo, "_b13")
  } else if (is.null(boundary_year) & geo != "councildist"){
    read_geos(geo, "")
  } else if (geo != "councildist"){
    message("`boundary_year` is only relevant for `geo = councildist`. Overriding boundary_year input to NULL")
    read_geos(geo, "")
  } else if ((boundary_year != "2013" & boundary_year != "2023") & geo == "councildist") {
    message("`boundary_year` must be '2013' or '2023'. Overriding boundary_year input to 2013.")
    read_geos(geo, "_b13")
  } else if (geo == "councildist"){
    read_geos(geo, glue::glue("_b{boundary_year_num}"))
  }
}
