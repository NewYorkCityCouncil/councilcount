#' Function to retrieve the available ACS demographic variables and their codes for a specified survey year
#'
#' @param acs_year (string). the desired 5-Year ACS year (ex: for the 2017-2021 5-Year ACS, enter '2021')
#' @return dataframe of available variables
#' @import tidyverse
#' @export

acs_years <- c('2011', '2016', '2021')

get_ACS_variables <- function(acs_year) {

  # warning message if unavailable survey year selected
  if (!(acs_year %in% acs_years)) {
    message("This ACS survey year is not available.", "\n",
            "Please choose from the following:\n",
            paste0('"',acs_years, '"', collapse = "\n"))
  }

  # Construct the name of the data dictionary based on the ACS year
  dict_name <- paste0("data_dictionary_", acs_year)

  # Retrieve the data dictionary from the package
  data_dictionary <- get(dict_name, envir = asNamespace("councilcount"))

  # Return the data dictionary
  return(data_dictionary)
}

