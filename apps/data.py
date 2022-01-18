import pandas as pd
import pathlib

# ------------------------------------------------------------------------------
# Data Processing

# get relative data folder
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../data").resolve()

# load the latest data
data = pd.read_csv(DATA_PATH.joinpath("owid-covid-data.csv"))
# filter data down to only columns we need
data = data[['iso_code', 'location', 'date', 'total_cases', 'new_cases', 'total_cases_per_million',
             'new_cases_per_million', 'total_deaths', 'new_deaths', 'total_deaths_per_million',
             'new_deaths_per_million', 'total_tests', 'new_tests', 'total_tests_per_thousand',
             'new_tests_per_thousand', 'total_vaccinations', 'new_vaccinations', 'total_vaccinations_per_hundred',
             'new_vaccinations_smoothed_per_million']]
# convert date column to datetime
data['date'] = pd.to_datetime(data.date)

# compute weekly data
weekly_data = data.groupby(['iso_code', 'location']).rolling(7, on='date').sum().reset_index()

# generate marks for date range slider
marks = {int(i): str(j)[:10] for i, j in enumerate(sorted(data.date.unique()))}
