#!/usr/bin/env Rscript
# Query DateLife for the age of the most recent common ancestor (MRCA) of a set of taxa,
# using the chronogram database bundled with the datelife R package (built from Open
# Tree of Life's phylesystem, which is CC0).
#
# Usage:
#   Rscript datelife_query.R "Amborella trichopoda" "Arabidopsis thaliana" "Oryza sativa"
#   Rscript datelife_query.R --yaml "Homo sapiens" "Ornithorhynchus anatinus"
#
# Prints a JSON object (or, with --yaml, a block ready to paste into README.yaml) with the
# median, min and max MRCA age across all chronograms that contain the MRCA, the number
# of chronograms, and the citations of the source studies.
#
# Choose taxa that span the root of the INGROUP of the dataset (not the outgroups), so
# the MRCA age is the age of the ingroup crown group. Two or three well-known species
# from the most distantly related lineages in the ingroup usually works best.

suppressPackageStartupMessages({
  library(datelife)
  library(jsonlite)
})

args <- commandArgs(trailingOnly = TRUE)
as_yaml <- "--yaml" %in% args
taxa <- args[args != "--yaml"]
if (length(taxa) < 2) {
  stop("Give at least two taxon names (quote names containing spaces).")
}

# use_tnrs = TRUE resolves names through Open Tree's taxonomy service (needs network);
# fall back to exact matching if that fails.
query <- tryCatch(
  make_datelife_query(input = taxa, use_tnrs = TRUE),
  error = function(e) make_datelife_query(input = taxa, use_tnrs = FALSE)
)
res <- datelife_search(input = query, summary_format = "mrca")

if (is.null(res) || length(res) == 0 || all(is.na(res))) {
  out <- list(source = "datelife", query_taxa = paste(taxa, collapse = ", "),
              date_accessed = format(Sys.Date(), "%Y-%m-%d"),
              median_age = "NA", min_age = "NA", max_age = "NA",
              n_chronograms = "NA", source_studies = "NA",
              note = "DateLife found no chronogram containing the MRCA of these taxa")
} else {
  ages <- as.numeric(res)
  studies <- names(res)
  fmt <- function(x) paste(format(round(x, 1), nsmall = 1), "mya")
  out <- list(source = "datelife", query_taxa = paste(taxa, collapse = ", "),
              date_accessed = format(Sys.Date(), "%Y-%m-%d"),
              median_age = fmt(median(ages)), min_age = fmt(min(ages)), max_age = fmt(max(ages)),
              n_chronograms = length(ages),
              source_studies = paste(unique(studies), collapse = " | "),
              ages_by_study = as.list(setNames(round(ages, 2), studies)))
}

if (as_yaml) {
  cat("    divergence time:\n")
  cat("        source: datelife\n")
  cat("        query taxa: \"", out$query_taxa, "\"\n", sep = "")
  cat("        date accessed: ", out$date_accessed, "\n", sep = "")
  cat("        median age: ", out$median_age, "\n", sep = "")
  cat("        min age: ", out$min_age, "\n", sep = "")
  cat("        max age: ", out$max_age, "\n", sep = "")
  cat("        N chronograms: ", out$n_chronograms, "\n", sep = "")
  cat("        source studies: \"", gsub('"', "'", out$source_studies), "\"\n", sep = "")
} else {
  cat(toJSON(out, auto_unbox = TRUE, pretty = TRUE), "\n")
}
