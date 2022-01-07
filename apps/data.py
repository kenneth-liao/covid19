import pandas as pd

# ------------------------------------------------------------------------------
# Data Processing

# load the latest data
data = pd.read_csv('data/owid-covid-data.csv')
# filter data down to only columns we need
data = data[['iso_code', 'location', 'date', 'total_cases', 'new_cases', 'total_cases_per_million',
             'new_cases_per_million', 'total_deaths', 'new_deaths', 'total_deaths_per_million',
             'new_deaths_per_million', 'total_tests', 'new_tests', 'total_tests_per_thousand',
             'new_tests_per_thousand', 'total_vaccinations', 'new_vaccinations', 'total_vaccinations_per_hundred',
             'new_vaccinations_smoothed_per_million']]
