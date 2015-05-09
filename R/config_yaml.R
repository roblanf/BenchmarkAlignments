# configuration for YAML parser

validSectionNames   <- c("study", "dataset")
validStudyKeys      <- c("reference", "year", "DOI")
validDatasetKeys    <- c("DOI", "license", "used for tree inference",
                         "timetree root age", "study root age", "study clade", "notes")
validLicenseKeys    <- c("type", "notes")
validStudyCladeKeys <- c("latin", "english", "taxon ID")
taxonUrlStub        <- "http://www.ncbi.nlm.nih.gov/Taxonomy/Browser/wwwtax.cgi?mode=Info&id="
doiUrlStub          <- "dx.doi.org"


# ######################################################################################
# DO NOT EDIT BELOW THIS POINT

library(testthat)
sourcePath <- getwd()

checkYAML <- function(yaml) {
  # TODO - cope with trailing / on path
  if (!file.exists(yaml)) stop(paste0("File '", yaml, "' does not exist!"), call. = FALSE)
  if (file.info(yaml)$isdir) {
    yamlFiles <- list.files(path = yaml, pattern = "yaml", full.names = TRUE, recursive = TRUE)
  } else {
    yamlFiles <- yaml
  }
  for (i in 1:length(yamlFiles)) {
    yamlFileName <<- yamlFiles[i]
    res <<- test_file(paste0(sourcePath, "/check_yaml.R"), reporter = new("SilentReporter")) #new("SilentReporter")) #"summary"
    showResults(res)
    message("")
  }
}
