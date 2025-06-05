import pandas as pd
import os
import numpy as np
from transformation.connection import engine

# Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_CSV = os.path.join(BASE_DIR, 'data', 'raw', 'covid_data.csv')
PROCESSED_CSV = os.path.join(BASE_DIR, 'data', 'processed', 'covid_data_cleaned.csv')

# Read CSV with proper quotechar handling
df = pd.read_csv(RAW_CSV, quotechar='"')

# Remove leading/trailing spaces from strings
def strip_strings(df):
    for col in df.select_dtypes(include='object').columns:
        df[col] = df[col].str.strip()
    return df

df = strip_strings(df)

# Replace 'N/A' and empty strings with NaN
df.replace(['N/A', ''], np.nan, inplace=True)

# Drop fully empty rows or rows with only NaNs
df.dropna(how='all', inplace=True)

# Clean numeric columns
def clean_numeric_column(df, column):
    if column in df.columns:
        df[column] = df[column].astype(str).str.replace(",", "").str.strip()
        df[column] = pd.to_numeric(df[column], errors='coerce')

numeric_cols = [
    'Total Cases', 'New Cases', 'Total Deaths', 'New Deaths',
    'Total Recovered', 'New Recovered', 'Active Cases', 'Serious, Critical',
    'Tot Cases/ 1M pop', 'Deaths/ 1M pop', 'Total Tests', 'Tests/ 1M pop', 'Population',
    'New Cases/1M pop', 'New Deaths/1M pop', 'Active Cases/1M pop'
]

for col in numeric_cols:
    clean_numeric_column(df, col)

# Rename columns for consistency
df.rename(columns={
    'Country, Other': 'Country',
    'Total Cases': 'TotalCases',
    'New Cases': 'NewCases',
    'Total Deaths': 'TotalDeaths',
    'New Deaths': 'NewDeaths',
    'Total Recovered': 'TotalRecovered',
    'New Recovered': 'NewRecovered',
    'Active Cases': 'ActiveCases',
    'Serious, Critical': 'SeriousCritical',
    'Tot Cases/ 1M pop': 'CasesPer1M',
    'Deaths/ 1M pop': 'DeathsPer1M',
    'Total Tests': 'TotalTests',
    'Tests/ 1M pop': 'TestsPer1M',
    'New Cases/1M pop': 'NewCasesPer1M',
    'New Deaths/1M pop': 'NewDeathsPer1M',
    'Active Cases/1M pop': 'ActiveCasesPer1M'
}, inplace=True)

# Add derived columns
if 'TotalDeaths' in df.columns and 'TotalCases' in df.columns:
    df['MortalityRate'] = df['TotalDeaths'] / df['TotalCases']
    df['MortalityRate'].fillna(0, inplace=True)

# Save cleaned data
df.to_csv(PROCESSED_CSV, index=False)
df.to_sql("covid_data", con=engine, if_exists='replace', index=False)

print(f"Cleaned data saved to {PROCESSED_CSV}")
