import pandas as pd

def clean_sales_data(input_file, output_file):
    try:
        df = pd.read_csv(input_file, encoding='ISO-8859-1')
    except Exception as e:
        print(f"Error reading file: {e}")
        return None

    # Handle missing values
    df = df.fillna({'ADDRESSLINE2': '', 'STATE': '', 'POSTALCODE': '', 'TERRITORY': 'Unknown'})
    numeric_cols = df.select_dtypes(include='number').columns
    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].median())

    # Standardize text fields
    text_columns = ['COUNTRY', 'STATUS', 'DEALSIZE', 'PRODUCTLINE', 'CITY', 'CUSTOMERNAME', 
                    'PRODUCTCODE', 'ADDRESSLINE1', 'ADDRESSLINE2', 'STATE', 'POSTALCODE', 
                    'TERRITORY', 'CONTACTLASTNAME', 'CONTACTFIRSTNAME']
    
    for col in text_columns:
        if col in df.columns:
            df[col] = df[col].astype(str).str.lower().str.strip().str.replace(r'[\r\n\t]', '', regex=True)

    # Convert date column
    if 'ORDERDATE' in df.columns:
        df['ORDERDATE'] = pd.to_datetime(df['ORDERDATE'], errors='coerce')
        df = df.dropna(subset=['ORDERDATE'])

    # Rename all columns to lowercase with underscores
    df.columns = df.columns.str.lower().str.replace(' ', '_')

    # Convert numeric columns
    numeric_cols = ['quantityordered', 'priceeach', 'sales', 'msrp']
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')

    # Create new column for total order value
    if 'quantityordered' in df.columns and 'priceeach' in df.columns:
        df['total_order_value'] = df['quantityordered'] * df['priceeach']

    # Remove duplicates 
    key_cols = ['ordernumber', 'productcode', 'orderlinenumber']
    df = df.drop_duplicates(subset=key_cols, keep='first')

    # Save the cleaned dataset
    try:
        df.to_csv(output_file, index=False)
        print(f" Cleaned data saved to {output_file}")
    except Exception as e:
        print(f" Error saving cleaned data: {e}")
        return None

    return df

if __name__ == "__main__":
    input_file = "sales_data_sample.csv"
    output_file = "sales_data_cleaned.csv"
    cleaned_data = clean_sales_data(input_file, output_file)
