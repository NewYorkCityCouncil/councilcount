#' A dataframe containing BBL-level population estimates for a specified year
#'
#' @import dplyr
#' @param year (string). The desired year for BBL-level estimates
#' @return tibble with PLUTO bbl population estimates
#' @export
#'

acs_years <- c('2011', '2016', '2021')

get_bbl_estimates <- function(year) {

  # Warning message if unavailable survey year selected
  if (!(year %in% acs_years)) {
    message("This year is not available.", "\n",
            "Please choose from the following:\n",
            paste0('"', acs_years, '"', collapse = "\n"))
  }

  # Construct the name of the dataset based on the year
  bbl_name <- paste0("bbl-population-estimates_", year, '.csv')

  # Retrieve the dataset from the package
  readr::read_csv(fs::path_package("extdata", glue::glue(bbl_name), package = "councilcount")) %>%
    janitor::clean_names()

  }
