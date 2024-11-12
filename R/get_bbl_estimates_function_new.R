#' A dataframe containing BBL-level population estimates for a specified year
#'
#' @import tidyverse
#' @import dplyr
#' @param year (string). The desired year for BBL-level estimates
#' @return tibble with PLUTO bbl population estimates
#' @export
#'

get_bbl_estimates <- function(year = NULL) {

  # find all the available years
  csv_names <- dir(system.file("extdata", package = "councilcount"))
  bbl_csv_names <- csv_names[grepl("bbl-population-estimates_", csv_names)]
  bbl_years <- sapply(bbl_csv_names, function(x) substr(x, 26, 29))

  # if year not chosen, set default to latest year
  if (is.null(year)){
    year <- max(bbl_years)
  }

  # construct the name of the dataset based on the year
  bbl_name <- paste0("bbl-population-estimates_", year, '.csv')

  # error message if unavailable survey year selected
  if (!(year %in% bbl_years)) {
    stop("This year is not available.", "\n",
         "Please choose from the following:\n",
         paste0('"', bbl_years, '"', collapse = "\n"))
  }

  print(paste('Printing BBL-level population estimates for', year))

  # retrieve the dataset from the package
  readr::read_csv(fs::path_package("extdata", glue::glue(bbl_name), package = "councilcount")) %>%
    janitor::clean_names()

}
