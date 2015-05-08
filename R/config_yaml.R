# configuration for YAML parser

validSectionNames   <- c("study", "dataset")
validStudyKeys      <- c("reference", "year", "DOI")
validDatasetKeys    <- c("DOI", "license", "used for tree inference",
                         "timetree root age", "study root age", "study clade", "notes")
validLicenseKeys    <- c("type", "notes")
validStudyCladeKeys <- c("latin", "english", "taxon ID")
taxonUrlStub        <- "http://www.ncbi.nlm.nih.gov/Taxonomy/Browser/wwwtax.cgi?mode=Info&id="


# ######################################################################################
# DO NOT EDIT BELOW THIS POINT

library(testthat)
sourcePath <- getwd()

checkYAML <- function(yaml) {
  if (!file.exists(yaml)) stop(paste0("File '", yaml, "' does not exist!"), call. = FALSE)
  #assign("yamlFileName", yaml, envir = .GlobalEnv)
  yamlFileName <<- yaml
  res <<- test_file(paste0(sourcePath, "/check_yaml.R"), reporter = new("SilentReporter")) #new("SilentReporter")) #"summary"
  showResults(res)
  message("")
}
