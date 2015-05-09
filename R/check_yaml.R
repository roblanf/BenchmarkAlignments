# perform validation tests on YAML file
# called from config_yaml.R

library(yaml)
library(RCurl)

# returns current year
getCurrentYear <- function() {
  as.integer(format(Sys.time(), "%Y"))
}

#yamlFileName <- "~/Work/nexus/PartitionedAlignments/datasets/Anderson_2013/README.yaml"  # testing only
options(warn = -1)
y <- yaml.load_file(yamlFileName)
options(warn = 1)

context("[Read YAML file]")

test_that(" YAML file was read successfully", {
  expect_true(exists("y"))
})

context("[Top-level structure]")

test_that(" number of sections is correct", {
  expect_equal(length(validSectionNames), length(y))
})

test_that(" section names are all present", {
  expect_equal(setdiff(validSectionNames, names(y)), character(0))
})

test_that(" sections are in preferred order", {
  expect_equal(validSectionNames, names(y))
})

context("[study]")
s <- y$study

test_that(" number of keys is correct", {
  expect_equal(length(validStudyKeys), length(s))
})

test_that(" keys are all present", {
  expect_equal(setdiff(validStudyKeys, names(s)), character(0))
})

test_that(" keys are in preferred order", {
  expect_equal(validStudyKeys, names(s))
})

test_that("[study$reference] is a valid character string", {
  expect_is(s$reference, "character")
})

test_that("[study$reference] has length > 0", {
  expect_true(nchar(s$reference) > 0)
})

test_that("[study$year] is a valid year", {
  expect_is(s$year, "integer")
  expect_true(s$year >= 1900 & s$year <= getCurrentYear())
})

studyDOI <- s$DOI

test_that("[study$DOI] is a valid DOI URL", {
  expect_true(grepl("^dx.doi.org", s$DOI, fixed = FALSE))
})

test_that("[study$DOI] URL resolves", {
  expect_true(url.exists(s$DOI))
})

context("[dataset]")
d <- y$dataset

test_that("[dataset] number of keys is correct", {
  expect_equal(length(validDatasetKeys), length(d))
})

test_that("[dataset] keys are all present", {
  expect_equal(setdiff(validDatasetKeys, names(d)), character(0))
})

test_that("[dataset] keys are in preferred order", {
  expect_equal(validDatasetKeys, names(d))
})

test_that("[dataset$DOI] is valid DOI URL", {
  expect_true(grepl(paste0("^", doiUrlStub), d$DOI, fixed = FALSE) | d$DOI == "NA")
})

test_that("[dataset$DOI] URL resolves", {
  expect_true(url.exists(d$DOI))
})

datasetDOI <- d$DOI

test_that("[dataset$DOI] differs from study DOI", {
  expect_true(studyDOI != datasetDOI)
})

test_that("[dataset$used for tree inference] is 'yes' or 'no'", {
  expect_true(d$'used for tree inference' %in% c("yes", "no"))
})

test_that("[dataset$timetree root age] is integer(mya) or NA", {
  expect_match(d$'timetree root age', "(^[0-9]+ *(mya)*$)|(^NA$)")
})

test_that("[dataset$study root age] is integer(mya) or NA", {
  expect_match(d$'study root age', "(^[0-9]+(mya| mya)?$)|(^NA$)")
})

test_that("[dataset$notes] is text", {
  expect_is(d$notes, "character")
})

test_that("[dataset$notes] has length > 0", {
  expect_true(nchar(d$notes) > 0)
})

context("[license]")
l <- d$license

test_that("[license] number of keys is correct", {
  expect_equal(length(validLicenseKeys), length(l))
})

test_that("[license] keys names are all present", {
  expect_equal(setdiff(validLicenseKeys, names(l)), character(0))
})

test_that("[license] keys are in preferred order", {
  expect_equal(validLicenseKeys, names(l))
})

test_that("[license$type] type is CC0", {
  expect_equal(l$type, "CC0")
})

if (grepl("/dryad.", datasetDOI, fixed = TRUE)) {
  test_that("[license$notes] is NA (dryad)", {
    expect_equal(l$notes, "NA")
  })
} else {
  test_that("[license$notes] is text (non-dryad)", {
    expect_true(l$notes != "NA" & nchar(l$notes) > 0)
  })  
}

context("[study clade]")
sc <- d$'study clade'

test_that("[study clade] number of keys is correct", {
  expect_equal(length(validStudyCladeKeys), length(sc))
})

test_that("[study clade] key names are all present", {
  expect_equal(setdiff(validStudyCladeKeys, names(sc)), character(0))
})

test_that("[study clade] keys are in preferred order", {
  expect_equal(validStudyCladeKeys, names(sc))
})

test_that("[study clade$latin] is one title-case word", {
  expect_match(sc$latin, "^[A-Z][a-z]+$")
})

test_that("[study clade$english] is one or more words", {
  expect_true(nchar(sc$english) > 0)
})

test_that("[study clade$taxon ID] is an integer", {
  expect_is(sc$'taxon ID', "integer")
})

test_that("[study clade$taxon ID] URL resolves", {
  expect_true(url.exists(paste0(taxonUrlStub, sc$'taxon ID')))
})

### end of tests ###

# global function to present results to user
showResults <<- function(res) {
  if (nrow(res[res$failed == 1, ]) == 0) {
    message(paste0("\nThe file '", yamlFileName, "' passed all tests! Well done!"))
  } else {
    message(paste0("\nThe following test(s) failed when checking file '", yamlFileName, "':\n"))
    apply(res[res$failed == 1, c("context", "test")], 1, message)
  }   
}

