#The purpose of this script is to clean and preprocess sales data for presentation.
import pandas as pd
import numpy as np

#Retrieve data from CSV file in data/raw folder
def load_data(file_path: str):
    df = pd.read_csv(file_path)
    return df
# File path to the raw sales data
file_path = 'data/raw/sales_data_raw.csv'

# Cleaning functions
# Clean column names to capitalize names and replace spaces with underscores
def clean_column_names(df):
    df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')
    df.columns = df.columns.str.replace('_', ' ').str.title()
    return df

#Handles missing prices and quantities using drop
def handle_missing_values(df, price_col, quantity_col):
    df = df.dropna(subset=[price_col, quantity_col])
    return df
#Removes rows with invalid values
def remove_invalid_rows(df, price_col, quantity_col):
    df[price_col] = pd.to_numeric(df[price_col], errors='coerce')
    df[quantity_col] = pd.to_numeric(df[quantity_col], errors='coerce')
    df = df[(df[price_col] >= 0) & (df[quantity_col] >= 0)]
    return df

# Load and clean the dataframe
df = load_data(file_path)
df = clean_column_names(df)
df = handle_missing_values(df, 'Price', 'Qty')
df = remove_invalid_rows(df, 'Price', 'Qty')

# Display the cleaned dataframe
print(df.head())