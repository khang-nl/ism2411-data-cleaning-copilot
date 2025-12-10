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
#Cleans product names and categories (removes quotes, extra spaces, capitalizes, combines duplicates)
def clean_product_data(df, product_col, category_col):
    # Normalize product names FIRST for grouping
    df['_normalized'] = df[product_col].str.lower().str.strip().str.replace(' +', ' ', regex=True)
    
    # Helper function to capitalize product names properly (handling acronyms)
    def capitalize_product_name(name):
        # Special handling for known acronyms
        if 'usb' in name.lower():
            return name.lower().replace('usb', 'USB').title().replace('Usb', 'USB')
        return name.strip().title()
    
    # Group by normalized product name and combine data
    def clean_category(x):
        # Clean and get first non-empty category
        cleaned = x.str.strip().str.replace('"', '').str.title()
        non_empty = cleaned[cleaned.str.len() > 0]
        return non_empty.iloc[0] if len(non_empty) > 0 else cleaned.iloc[0]
    
    grouped = df.groupby('_normalized', as_index=False).agg({
        product_col: lambda x: capitalize_product_name(x.iloc[0]),
        category_col: clean_category,
        'Price': lambda x: pd.to_numeric(x, errors='coerce').dropna().max() if len(pd.to_numeric(x, errors='coerce').dropna()) > 0 else np.nan,
        'Qty': lambda x: pd.to_numeric(x, errors='coerce').sum(),
        'Date Sold': lambda x: x[x.str.strip().str.len() > 0].iloc[0] if len(x[x.str.strip().str.len() > 0]) > 0 else x.iloc[0]
    }).drop(columns=['_normalized'])
    
    return grouped
#Removes rows with invalid values
def remove_invalid_rows(df, price_col, quantity_col):
    df[price_col] = pd.to_numeric(df[price_col], errors='coerce')
    df[quantity_col] = pd.to_numeric(df[quantity_col], errors='coerce')
    df = df[(df[price_col] >= 0) & (df[quantity_col] >= 0)]
    return df

# Load and clean the dataframe
df = load_data(file_path)
df = clean_column_names(df)
df = clean_product_data(df, 'Prodname', 'Category')
df = handle_missing_values(df, 'Price', 'Qty')
df = remove_invalid_rows(df, 'Price', 'Qty')
df = df.reset_index(drop=True)

# Saves cleaned data to a new CSV file in data/processed folder
if __name__ == "__main__":
    raw_path = "data/raw/sales_data_raw.csv"
    cleaned_path = "data/processed/sales_data_clean.csv"

    df_raw = load_data(raw_path)
    df_clean = clean_column_names(df_raw)
    df_clean = clean_product_data(df_clean, 'Prodname', 'Category')
    df_clean = handle_missing_values(df_clean, 'Price', 'Qty')
    df_clean = remove_invalid_rows(df_clean, 'Price', 'Qty')
    df_clean = df_clean.reset_index(drop=True)
    df_clean.to_csv(cleaned_path, index=False)
    print("Cleaning complete. First few rows:")
    print(df_clean.head())