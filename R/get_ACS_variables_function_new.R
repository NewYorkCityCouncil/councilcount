#' Function to retrieve the available ACS demographic variables and their codes for a specified survey year
#'
#' @import tidyverse
#' @param acs_year (string). The desired 5-Year ACS year (ex: for the 2017-2021 5-Year ACS, enter '2021')
#' @return dataframe of available variables
#' @export

get_ACS_variables <- function(acs_year) {

  # find all the available years
  csv_names <- dir(system.file("extdata", package = "councilcount"))
  dictionary_csv_names <- csv_names[grepl("data_dictionary", csv_names)]
  dictionary_years <- sapply(dictionary_csv_names, function(x) substr(x, 17, 20))

  # construct the name of the dataset based on the year
  dict_name <- paste0("data_dictionary_", acs_year, '.csv')

  # error message if unavailable survey year selected
  if (!(acs_year %in% dictionary_years)) {
    stop("This year is not available.", "\n",
         "Please choose from the following:\n",
         paste0('"', dictionary_years, '"', collapse = "\n"))
  }

  # Retrieve the data dictionary from the package
  readr::read_csv(fs::path_package("extdata", glue::glue(dict_name), package = "councilcount")) %>%
    janitor::clean_names()

}


