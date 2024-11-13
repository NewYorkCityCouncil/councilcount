#' Function to retrieve the available ACS demographic variables and their codes for a specified survey year
#'
#' @import tidyverse
#' @import dplyr
#' @param acs_year (string). The desired 5-Year ACS year (ex: for the 2017-2021 5-Year ACS, enter "2021"). The most recent year available will populate if left NULL.
#' @return Table of available variables with columns for variable code, variable name, denominator code, and denominator name (the "denominator variable" is the denominator population in percent estimate calculations). Use variable codes as the input for `var_codes` in get_geo_estimates().
#' @export

get_ACS_variables <- function(acs_year = NULL) {

  # find all the available years
  csv_names <- dir(system.file("extdata", package = "councilcount"))
  dictionary_csv_names <- csv_names[grepl("data_dictionary", csv_names)]
  dictionary_years <- sapply(dictionary_csv_names, function(x) substr(x, 17, 20))

  # if year not chosen, set default to latest year
  if (is.null(acs_year)){
    acs_year <- max(dictionary_years)
  }

  # construct the name of the dataset based on the year
  dict_name <- paste0("data_dictionary_", acs_year, '.csv')

  # error message if unavailable survey year selected
  if (!(acs_year %in% dictionary_years)) {
    stop("This year is not available.", "\n",
         "Please choose from the following:\n",
         paste0('"', dictionary_years, '"', collapse = "\n"))
  }

  print(paste('Printing data dictionary for the', acs_year, '5-Year ACS'))

  # Retrieve the data dictionary from the package
  readr::read_csv(fs::path_package("extdata", glue::glue(dict_name), package = "councilcount")) %>%
    janitor::clean_names()

}


