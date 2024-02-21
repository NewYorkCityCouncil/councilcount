#' Function to retrieve PLUTO bbl population estimates
#'
#' @import dplyr
#' @return tibble with PLUTO bbl population estimates
#' @export
#'

get_bbl_estimates <- function() {
  readr::read_csv(fs::path_package("extdata", glue::glue("bbl-population-estimates_2021.csv"), package = "councilcount")) %>%
    janitor::clean_names()
  }
