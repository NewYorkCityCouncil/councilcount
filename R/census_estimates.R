#' View available census variables and their descriptions
#'
#' @param as_df boolean. \code{as_df = TRUE} to return a dataframe. \code{as_df = FALSE} to just print. default \code{as_df = TRUE}
#' @import reticulate
#' @return Either a DataFrame or printed census variable codes and their description
#' @export
#' @examples
#' \dontrun{
#' library(councilverse)
#' view_ACS_variables()
#' view_ACS_variables(as_df = FALSE)
#' }

view_ACS_variables <- function(as_df = TRUE){
  #use_python("/usr/local/bin/python3")
  source_python('python/retrieve_estimates.py')

  view_variables(as_df = as_df,demo_dict = py$census_demo_variables)
}


#' Get estimates for census variables for specified geographies
#'
#'
#' @param var_code_list vector or list. All the variable codes of interest
#' @param geo string. Desired geographic boundaries (options: council, policeprct, schooldist, cd, nta, schooldist, borough, nyc)
#' @param polygons boolean. \code{polygons = TRUE} to add geometry column. default \code{polygons = FALSE}
#' @param download boolean. \code{download = TRUE} to download output df to current working directory as csv. default \code{download = FALSE}
#'
#' @import reticulate
#' @return DataFrame of requested variables
#'
#' @export
#' @examples
#' \dontrun{
#' library(councilverse)
#' get_ACS_demographic_estimates(c("DP02_0078E","DP05_0002PE","DP05_0008PE"),geo = "nta",polygons = TRUE)
#' get_ACS_demographic_estimates("DP05_0008PE",geo = "council",download = TRUE)
#' }

get_ACS_demographic_estimates <- function(var_code_list, geo, polygons = FALSE, download = FALSE){
  #use_python("/usr/local/bin/python3")
  source_python('python/retrieve_estimates.py')

  var_code_list <- if(class(var_code_list) != "list") as.list(var_code_list)

  get_demo_estimates(var_code_list = var_code_list, geo = geo, polygons = polygon, download = download, demo_dict = py$census_demo_variables)

}


#' Get the Building Block Lot (BBL) level estimates for all available census variables
#'
#' @import reticulate
#' @return DataFrame of BBL level estimates
#' @export
#' @examples
#' \dontrun{
#' library(councilverse)
#' get_BBL_estimates()
#' }

get_BBL_estimates <- function(){
  #use_python("/usr/local/bin/python3")
  source_python('python/retrieve_estimates.py')

  get_bbl_estimates()
}




