# Install DateLife (https://github.com/phylotastic/datelife) into the benchaln env.
# DateLife is no longer on CRAN, so it is installed from the phylotastic r-universe
# after the conda env is built:
#   /path/to/envs/benchaln/bin/Rscript utility_scripts/install_datelife.R
options(repos = c(phylotastic = "https://phylotastic.r-universe.dev",
                  CRAN = "https://cloud.r-project.org"))
if (!requireNamespace("datelife", quietly = TRUE)) {
  install.packages("datelife")  # Depends/Imports only; compiled deps come from conda (environment.yml)
}
library(datelife)
cat("datelife", as.character(packageVersion("datelife")), "installed\n")
