#' Function to retrieve the available census demographic variables
#'
#'
#' @return data frame of available variables
#' @export
#'

# simply access census_demo_variables, can add functionality in the future if necessary
get_census_variables <- function() {
  councilcount::census_demo_variables %>%
    mutate(cleaned_name = janitor::make_clean_names(var_name))
  }
