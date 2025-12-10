import pandas as pd
import numpy as np
# Standardizes column names
def standardize_column_names(df):
    df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')
    return df
#Strip leading and trailing whitespace from names and categories
def strip_whitespace(df, columns):
    for col in columns:
        df[col] = df[col].str.strip()
    return df
#Handle missing prices and quantities with drop
def handle_missing_values(df, price_col, quantity_col):
    df = df.dropna(subset=[price_col, quantity_col])
    return df
#Remove rows with invalid values
def remove_invalid_values(df, price_col, quantity_col):
    df = df[(df[price_col] >= 0) & (df[quantity_col] >= 0)]
    return df

# Load and display the dataframe
df = pd.read_csv('../data/raw/sales_data_raw.csv')
print(df.head())