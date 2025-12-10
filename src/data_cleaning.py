import pandas as pd
import numpy as np

#Retrieve data from CSV file in data/raw folder
def load_data(file_path):
    df = pd.read_csv(file_path)
    return df

file_path = 'data/raw/sales_data_raw.csv'

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
    df[price_col] = pd.to_numeric(df[price_col], errors='coerce')
    df[quantity_col] = pd.to_numeric(df[quantity_col], errors='coerce')
    df = df[(df[price_col] >= 0) & (df[quantity_col] >= 0)]
    return df

# Load and clean the dataframe
df = load_data(file_path)
df = standardize_column_names(df)
df = handle_missing_values(df, 'price', 'qty')
df = remove_invalid_values(df, 'price', 'qty')

# Display the cleaned dataframe
print(df.head())