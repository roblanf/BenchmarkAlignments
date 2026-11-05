def pytest_addoption(parser):
    parser.addoption("--no-network", action="store_true", default=False,
                     help="skip DOI and NCBI Taxonomy lookups")
